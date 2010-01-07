# -*- coding: utf-8 -*-
"""
Milkshake
Copyright (C) 2009  Marcelo Barros & Jose Antonio Oliveira

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.


Milkshake
Copyright (C) 2009  Marcelo Barros & Jose Antonio Oliveira
This program comes with ABSOLUTELY NO WARRANTY; for details see 
about box.
This is free software, and you are welcome to redistribute it
under certain conditions; see about box for details.
"""

from appuifw import *
from window import Application, Dialog
import pickle
import os
import e32
import sysinfo
import sys
from about import About
from taskutil import *
from edittask import EditTask
from settings import MSSettings, Config
import copy
import time
from mseplugin import MSExportPlugin

__all__ = [ "Milkshake" ]
__author__  = "José Antonio (javsmo@gmail.com) and "
__author__ += "Marcelo Barros de Almeida (marcelobarrosalmeida@gmail.com)"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2009- Javsmo/Marcelo"
__license__ = "GPLv3"
   
class Milkshake(Application):
    MSDEFDIR = u""
    MSDBNAME = u""
    MSICONNAME = u""
    MSVERSION = u"0.1.0"
    def __init__(self,path=u"e:\\python"):
        Milkshake.MSDEFDIR = path
        Milkshake.MSDBNAME = os.path.join(path,u"milkshake.bin")
        Milkshake.MSICONNAME = os.path.join(path,u"milkshake.mif")
        sys.path.append(os.path.join(Milkshake.MSDEFDIR,u"plugins",u"export"))
        sys.path.append(os.path.join(Milkshake.MSDEFDIR,u"plugins",u"import"))
        app.screen = 'normal'
        app.directional_pad = False
        self.list_mngr = ListManager()
        self.config = Config()
        self.load_cfg()
        self.load_icons()
        self.tabs_active = False
        self.main_menu = [(u"Save",self.save_cfg),
                          (u"Settings ...",self.settings_dlg),
                          (u"Export ...",self.plugins_export),
                          (u"Import ...",self.plugins_import),
                          (u"Syncronize ...",self.sync_dlg),
                          (u"About", self.about_ms),
                          (u"Exit", self.close_app)]
        Application.__init__(self, u"Milkshake", Listbox([(u"",u"")],lambda:None), [])
        self.update_lists()

    def update_lists(self,lst_pos=None,pos=None):
        if not self.tabs_active:
            menu = [(u"Lists ...", self.list_menu)]+self.main_menu
            self.set_ui(u"Milkshake", Listbox(self.get_task_list_list(),self.edit_tasks), menu)
        else:
            app_data = []
            menu = [(u"Lists ...", self.list_menu),
                    (u"Tasks ...",self.task_menu)] + self.main_menu
            for lst in self.list_mngr.keys():
                # set filter for done tasks
                self.show_done_tasks(lst,self.config['show_done'])
                app_data.append((lst,Listbox(self.get_task_list(lst),self.task_menu),[])) 
            self.set_ui(u"Milkshake", app_data, menu, self.edit_tasklist)
            if lst_pos is not None:
                self.last_tab = lst_pos
        self.refresh()

    def edit_tasks(self):
        self.tabs_active = True
        n = app.body.current()
        self.update_lists(n)

    def edit_tasklist(self):
        self.tabs_active = False
        self.update_lists()        
        
    def get_def_task_list_mngr(self):
        lst = ListManager()
        lst[u"Default"] = TaskList()
        return lst

    def get_task_list_list(self):
        lst = []
        for k in self.list_mngr.keys():
            if self.config['single_row']:
                lst.append(k)
            else:
                n = len(self.list_mngr[k])
                if n > 1:
                    m = u"%d tasks" % n
                elif n == 1:
                    m = u"%d task" % n
                else:
                    m = u"No tasks"
                lst.append((k,m))
        return lst

    def get_def_task_list(self):
        if self.config['single_row']:
            return [(u"Press select to add tasks",self.icons["none"])]
        else:
            return [(u"Press select to add tasks",u"",self.icons["none"])]
        
    def get_icon(self,tsk):
        return self.icons["%d-%d" % (tsk["pri"],tsk["perc_done"])]

    def get_task_list(self,lst):
        if self.list_mngr[lst]:
            if self.config['single_row']:
                tlst = [(tskn["name"],self.get_icon(tskn)) for tskn in self.list_mngr[lst]]
            else:
                tlst = []
                for t in self.list_mngr[lst]:
                    a = t["name"]
                    b = u"P%d  %d%%  " % (t['pri'],t['perc_done'])
                    if t['type'] == Task.FIXED_DATE:
                        b += unicode(time.strftime("%d/%b/%Y",time.localtime(t['due_date'])))
                    tlst.append((a,b,self.get_icon(t)))
        else:
            tlst = self.get_def_task_list()
        return tlst

    def load_icons(self):
        self.icons = {}
        for i in range(1,6):
            for p in range(0,21,2):
                n = (i-1)*22+p
                self.icons["%d-%d"%(i,int(10*p/2))] = Icon(Milkshake.MSICONNAME,n,n)
        self.icons["none"] = Icon(Milkshake.MSICONNAME,110,110)
        
    def load_cfg(self):
        try:
            f = open(Milkshake.MSDBNAME,"rb")
            version = pickle.load(f)
            self.list_mngr.load(f)
            self.config.load(f)
            f.close()
        except Exception, e:
            if os.path.exists(Milkshake.MSDBNAME):
                note(u"Impossible to load config from " +
                     Milkshake.MSDBNAME +
                     u". " + unicode(str(e)),"error")
            self.list_mngr = self.get_def_task_list_mngr()

    def save_cfg(self):
        try:
            f = open(Milkshake.MSDBNAME,"wb")
            pickle.dump(Milkshake.MSVERSION,f)
            self.list_mngr.save(f)
            self.config.save(f)
            f.close()
        except Exception, e:
            note(u"Impossible to save config to file " +
                 Milkshake.MSDBNAME +
                 u". " + unicode(str(e)),"error")

    def get_current_task_list(self):
        if self.tabs_active:
            lst = self.tab_title
        else:
            n = app.body.current()
            lst = self.list_mngr.keys()[n]
        return lst

    def list_menu(self):
        lst = self.get_current_task_list()
        menu = [(u"New",self.new_list),
                (u"Rename",self.ren_list),
                (u"Delete",self.del_list)]
        op = popup_menu([m[0] for m in menu],u"List menu:")
        if op is not None:
            menu[op][1](lst)

    def task_menu(self):
        lst = self.get_current_task_list()
        n = app.body.current()
        if self.list_mngr[lst]:
            menu = [(u"Edit",self.edit_task),
                    (u"New",self.new_task),
                    (u"Rename",self.ren_task),
                    (u"Delete",self.del_task)]
            if len(self.list_mngr.keys()) > 1:
                menu.append((u"Move",self.move_task))
            if self.list_mngr[lst][n]["perc_done"] < 100:
                    menu.append((u"Mark as done",self.done_task))
            else:
                    menu.append((u"Mark as not done",self.undone_task))
        else:
            menu = [(u"New",self.new_task)]
        op = popup_menu([m[0] for m in menu],u"Tasks menu:")
        if op is not None:
            menu[op][1](lst,n)
        
    def sync_dlg(self):
        note(u"Soon as possible ! Please, wait.","info")

    def new_list(self,lst):
        nlst = query(u"List name:","text",lst)
        if nlst is not None:
            if nlst in self.list_mngr.keys():
                note(u"This list name already exists !","error")
            else:
                self.list_mngr[nlst] = TaskList()
                self.update_lists()

    def del_list(self,lst):
        msg = u"Delete " + lst + u" ?"
        op = popup_menu([u"No", u"Yes"],msg)
        if op is not None:
            if op:
                del self.list_mngr[lst]
                if not self.list_mngr:
                    self.list_mngr = self.get_def_task_list_mngr()
                self.update_lists()

    def ren_list(self,lst):
        nlst = query(u"List name:","text",lst)
        if nlst is not None:
            self.list_mngr[nlst] = self.list_mngr[lst]
            del self.list_mngr[lst]
            self.update_lists()

    def new_task(self,lst,n):
        if self.list_mngr[lst]:
            tskn = self.list_mngr[lst][n]["name"]
        else:
            tskn = u""
        tsk = query(u"Task name:","text",tskn)
        if tsk is not None:
            self.list_mngr[lst].append(Task(name=tsk))
            lb = self.get_task_list(lst)
            app.body.set_list(lb,len(lb)-1)
            
    def del_task(self,lst,n):
        msg = u"Delete " + self.list_mngr[lst][n]["name"] + u" ?"
        op = popup_menu([u"No", u"Yes"],msg)
        if op is not None:
            if op:
                del self.list_mngr[lst][n]
                lb = self.get_task_list(lst)
                n = max(n - 1,0)
                app.body.set_list(lb,n)

    def ren_task(self,lst,n):
        tsk = query(u"Task name:","text",self.list_mngr[lst][n]["name"])
        if tsk is not None:
            self.list_mngr[lst][n]["name"] = tsk
            lb = self.get_task_list(lst)
            app.body.set_list(lb,app.body.current())

    def edit_task(self,lst,pos):
        def cbk():
            if not self.dlg.cancel:
                self.list_mngr[self.dlg.lst][self.dlg.pos] = self.dlg.tsk
            self.update_lists(self.dlg.lst_pos,self.dlg.pos)
        self.dlg = EditTask(cbk,self.list_mngr[lst][pos],lst,self.last_tab,pos)
        self.dlg.run()

    def move_task(self,lst,n):
        glst = [k for k in self.list_mngr.keys() if k != lst ]
        op = popup_menu(glst,u"To list:")
        if op is not None:
            nlst = glst[op] 
            self.list_mngr[nlst].append(self.list_mngr[lst][n])
            del self.list_mngr[lst][n]
            self.update_lists()

    def settings_dlg(self):
        def cbk():
            if not self.dlg.cancel:
                for k in self.config.keys():
                    self.config[k] = self.dlg.config[k]
            self.update_lists()
            return True
        self.dlg = MSSettings(cbk,copy.deepcopy(self.config))
        self.dlg.run()
        
    def show_done_tasks(self,lst,show):
        if show:
            self.list_mngr[lst].set_selection_filter(lambda t: True)
        else:
            self.list_mngr[lst].set_selection_filter(lambda t: t['perc_done'] < 100)
            
    def done_undone_task(self,lst,n,p):
        self.list_mngr[lst][n]['perc_done'] = p
        self.list_mngr[lst].update_filters()
        lb = self.get_task_list(lst)
        app.body.set_list(lb,n)

    def done_task(self,lst,n):
        self.done_undone_task(lst,n,100)

    def undone_task(self,lst,n):
        self.done_undone_task(lst,n,0)


    def try_import(self,module):            
        try:
            __import__(module)
        except:
            return False
        else:
            return True

    def load_plugins(self,pdir):
        plugins = []
        try:
            files = os.listdir(pdir)
        except:
            return plugins
        
        [ self.try_import(f[:f.rfind(".py")]) for f in files if f.endswith(".py") ]

        for plugin in MSExportPlugin.__subclasses__():
            if plugin not in plugins:
                # instanciate and add the plugin to the program
                plugins.append(plugin(self))
                #plugins[plugin].run(self.list_mngr)
        return plugins

    def run_plugins(self,plugin_type):
        pdir = os.path.join(Milkshake.MSDEFDIR,u"plugins",plugin_type)
        plugins = self.load_plugins(pdir)
        if plugins:
            names = [ p.get_name() for p in plugins ]
            op = popup_menu(names,u"Select plugin:")
            if op is not None:
                try:
                    plugins[op].run(self.list_mngr)
                except:
                    note(u"Impossible to run plugin " + plugins[op].get_name(),"error")
            del plugins
        else:
            note(u"You do not have any %s plugin " % plugin_type,"info")
            
    def plugins_export(self):
        self.run_plugins(u"export")

    def plugins_import(self):
        self.run_plugins(u"import")
    
    def about_ms(self):
        def cbk():
            self.refresh()
            return True
        self.dlg = About(cbk,Milkshake.MSVERSION)
        self.dlg.run()
    
    def close_app(self):
        ny = popup_menu([u"Yes", u"No"], u"Leave milkshake ?")
        if ny is not None:
            if ny == 0:
                self.save_cfg()
                Application.close_app(self)
                
if __name__ == "__main__":
    import sys
    sys.path.append(u"e:\\python")
    ms = Milkshake(u"e:\\python")
    ms.run()

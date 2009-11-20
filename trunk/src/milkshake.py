# -*- coding: utf-8 -*-

from appuifw import *
from window import Application, Dialog
import pickle
import os
import e32
from about import About

__all__ = [ "Milkshake" ]
__author__ = "José Antônio (javsmo@gmail.com) and "
__author__ = __author__ + "Marcelo Barros de Almeida (marcelobarrosalmeida@gmail.com)"
__version__ = "alpha1"
__copyright__ = "Copyright (c) 2009- Javsmo/Marcelo"
__license__ = "GPLv3"

class Notepad(Dialog):
    def __init__(self, cbk, grp, pos, txt=u"",):
        menu = [(u"Save", self.close_app),
                (u"Discard", self.cancel_app)]
        self.grp = grp
        self.pos = pos
        body = Text(txt)
        body.color = (200,200,200)
        body.style = STYLE_BOLD
        Dialog.__init__(self, cbk, grp, body, menu)
        
class Milkshake(Application):
    MSDEFDIR = u""
    MSDBNAME = u""
    MSVERSION = u"$Id:$"
    def __init__(self,path=u"e:\\python"):
        Milkshake.MSDEFDIR = path
        Milkshake.MSDBNAME = os.path.join(path,u"milkshake.bin")
        app.screen = 'normal'
        app.directional_pad = False
        self.load_cfg()
        self.common_menu = [ (u"New group",self.new_group),
                             (u"Rename group",self.ren_group),
                             (u"Del group",self.del_group),
                             (u"Save",self.save_cfg),
                             (u"Update", self.update_ms),
                             (u"About", self.about_ms),
                             (u"Exit", self.close_app) ]
        Application.__init__(self, u"Milkshake", Listbox([u""],lambda:None), self.common_menu)
        self.update_groups()

    def update_groups(self,grp=None,pos=None):
        app_data = []
        groups = self.tasks.keys()
        groups.sort()
        for grp in groups:
            app_data.append((grp,Listbox(self.get_tasknames(grp),self.group_cbk),[])) 
        self.set_ui(u"Milkshake", app_data, self.common_menu)
        self.refresh()
        
    def get_tasknames(self,grp):
        if self.tasks[grp]:
            return[tskn["name"] for tskn in self.tasks[grp]]
        else:
            return [u"Press select to add tasks"]

    def load_cfg(self):
        try:
            f = open(Milkshake.MSDBNAME,"rb")
            version = pickle.load(f)
            self.tasks = pickle.load(f)
            f.close()
        except:
            note(u"Impossible to load config from "+Milkshake.MSDBNAME,"error")
            self.tasks = { u"Default" : [] }

    def save_cfg(self):
        try:
            f = open(Milkshake.MSDBNAME,"wb")
            pickle.dump(MSVERSION,f)
            pickle.dump(self.tasks,f)
            f.close()
        except:
            note(u"Impossible to save config to file "+Milkshake.MSDBNAME,"error")

    def group_cbk(self):
        grp = self.tab_title
        if self.tasks[grp]:
            menu = [(u"Edit note",self.edit_note),
                    (u"Edit date",None),
                    (u"New task",self.new_task),
                    (u"Rename task",self.ren_task),
                    (u"Delete task",self.del_task)]
            if len(self.tasks.keys()) >1:
                menu.append((u"Move task",self.move_task))
        else:
            menu = [(u"New task",self.new_task)]
        n = app.body.current()
        op = popup_menu([m[0] for m in menu],u"Menu")
        if op is not None:
            menu[op][1](grp,n)
        
    def new_group(self):
        grp = query(u"Group name:","text",u"")
        if grp is not None:
            if grp in self.tasks.keys():
                note(u"This group name already exists !","error")
            else:
                self.tasks[grp] = []
                self.update_groups()

    def del_group(self):
        grp = self.tab_title
        msg = u"Delete " + grp + u" ?"
        op = popup_menu([u"No", u"Yes"],msg)
        if op is not None:
            if op:
                del self.tasks[grp]
                if not self.tasks:
                    self.tasks = { u"Default" : [] }
                self.update_groups()

    def ren_group(self):
        ogrp = self.tab_title
        grp = query(u"Group name:","text",ogrp)
        if grp is not None:
            # deep copy ?
            self.tasks[grp] = self.tasks[ogrp]
            del self.tasks[ogrp]
            self.update_groups()

    def new_task(self,grp,n):
        tsk = query(u"Task name:","text",u"")
        if tsk is not None:
            self.tasks[grp].append({"name":tsk,"note":u"","date":u""})
            lst = self.get_tasknames(grp)
            app.body.set_list(lst,len(lst)-1)
            
    def del_task(self,grp,n):
        msg = u"Delete " + self.tasks[grp][n]["name"] + u" ?"
        op = popup_menu([u"No", u"Yes"],msg)
        if op is not None:
            if op:
                del self.tasks[grp][n]
                lst = self.get_tasknames(grp)
                n = max(n - 1,0)
                app.body.set_list(lst,n)

    def ren_task(self,grp,n):
        tsk = query(u"Task name:","text",self.tasks[grp][n]["name"])
        if tsk is not None:
            self.tasks[grp][n]["name"] = tsk
            lst = self.get_tasknames(grp)
            app.body.set_list(lst,app.body.current())

    def edit_note(self,grp,pos):
        def cbk():
            if not self.dlg.cancel:
                self.tasks[self.dlg.grp][self.dlg.pos]["note"] = self.dlg.body.get()
            self.dlg = None
            self.refresh()
        self.dlg = Notepad(cbk,grp,pos,self.tasks[grp][pos]["note"])
        self.dlg.run()

    def move_task(self,grp,n):
        glst = [k for k in self.tasks.keys() if k != grp ]
        glst.sort()
        op = popup_menu(glst,u"To group:")
        if op is not None:
            ngrp = glst[op] 
            self.tasks[ngrp].append(self.tasks[grp][n])
            del self.tasks[grp][n]
            self.update_groups()

    def update_ms(self): pass
    def about_ms(self):
        def cbk():
            self.refresh()
            return True
        self.dlg = About(cbk,Milkshake.MSVERSION)
        self.dlg.run()
        
    def close_app(self):
        ny = popup_menu( [u"Yes", u"No"], u"Leave milkshake ?" )
        if ny is not None:
            if ny == 0:
                self.save_cfg()
                Application.close_app(self)
                
if __name__ == "__main__":
    import sys
    sys.path.append(u"e:\\python")
    ms = Milkshake(u"e:\\python")
    ms.run()

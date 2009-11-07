# -*- coding: utf-8 -*-
from appuifw import *
from window import Application, Dialog
import copy

__all__ = [ "Milkshake" ]
__author__ = "José Antônio (javsmo@gmail.com) and "
__author__ = __author__ + "Marcelo Barros de Almeida (marcelobarrosalmeida@gmail.com)"
__version__ = "alpha1"
__copyright__ = "Copyright (c) 2009- Javsmo/Marcelo"
__license__ = "GPLv3"

class Milkshake(Application):
    
    def __init__(self):
        app.screen = 'normal'
        app.directional_pad = False
        self.load_persistence()
        self.common_menu = [ (u"New Group", self.new_group),
                             (u"New Task", self.new_task),
                             (u"Update", self.update_rtm),
                             (u"Exit", self.close_app) ]
        Application.__init__(self, u"Milkshake", Listbox([u""],lambda:None), self.common_menu)
        self.update_groups()

    def update_groups(self):
        app_data = []
        keys = self.tasks.keys()
        keys.sort()
        for k in keys:
            # menus especificos aqui no []
            app_data.append((k,Listbox(self.tasks[k],self.group_cbk),[])) 
        self.set_ui(u"Milkshake", app_data, self.common_menu)
        self.refresh()
        
    def load_persistence(self):
        # no futuro, carregar tudo de um arquivo aqui
        self.tasks = { u"Group 1" : [ u"Task 11", u"Task 12", u"Task 13"],
                        u"Group 2" : [ u"Task 21", u"Task 22", u"Task 23"],
                        u"Group 3" : [ u"Task 31", u"Task 32", u"Task 33"] }

    def group_cbk(self):
        k = self.tab_title
        n = app.body.current()
        note(k+u": "+self.tasks[k][n],"info")
        
    def new_group(self): pass
    def new_task(self): pass
    def update(self): pass
    def update_rtm(self): pass

    def close_app(self):
        ny = popup_menu( [u"Yes", u"No"], u"Leave milkshake ?" )
        if ny is not None:
            if ny == 0:
                # salvar persistencia aqui
                Application.close_app(self)
                
if __name__ == "__main__":
    import sys
    sys.path.append(u"e:\python")

    ms = Milkshake()
    ms.run()

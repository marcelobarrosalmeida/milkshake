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

from window import Dialog
from taskutil import Task
import time
from appuifw import *

__all__ = [ "EditTask" ]

class Notepad(Dialog):
    def __init__(self, cbk, title, txt=u""):
        menu = [(u"Save", self.close_app),
                (u"Discard", self.cancel_app)]
        Dialog.__init__(self, cbk, title, Text(txt), menu)    

class EditTask(Dialog):
    def __init__(self, cbk, tsk, lst, lst_pos, pos):
        self.last_idx = 0
        self.lst = lst
        self.lst_pos = lst_pos
        self.pos = pos
        self.tsk = tsk
        Dialog.__init__(self, cbk, tsk['name'],
                        Listbox([(u"",u"")], self.update_value),
                        [(u"Cancel",self.cancel_app)])
    
    def refresh(self):
        def time2uni(tmr):
            return unicode(time.strftime("%d/%b/%Y",time.localtime(tmr)))
        values = [(u"Note",self.tsk['note'][:50]), 
                  (u"Name",self.tsk['name']),
                  (u"Priority",unicode(self.tsk['pri'])),
                  (u"Percent done",unicode(self.tsk['perc_done'])),
                  (u"Type",Task.TYPES_DESC[self.tsk['type']])]
        if self.tsk['type'] == Task.FIXED_DATE:
            values += [(u"Start date",time2uni(self.tsk['start_date'])),
                       (u"Due date",time2uni(self.tsk['due_date']))]
        self.body.set_list(values, self.last_idx)
        Dialog.refresh(self)

    def update_value(self):
        idx = app.body.current()
        self.last_idx = idx
        ops = [self.edit_note,
               self.edit_name,
               self.edit_pri,
               self.edit_perc_done,
               self.edit_type]
        if self.tsk['type'] == Task.FIXED_DATE:
            ops += [self.edit_start_date,
                    self.edit_due_date]
        # return True if you want a refresh and screen repaint
        if ops[idx]():
            self.refresh()
            
    def edit_name(self):
        name = query(u"Task name:","text",self.tsk["name"])
        if name is not None:
            self.tsk["name"] = name
        return True

    def edit_type(self):
        if self.tsk['type'] == Task.FIXED_DATE:
            self.tsk['type'] = Task.NO_DUE_DATE
        else:
            self.tsk['type'] = Task.FIXED_DATE
        return True
            
    def edit_pri(self):
        pri_ops = [u"1 (high)",u"2",u"3",u"4",u"5 (low)"]
        op = popup_menu(pri_ops,u"Priority:")
        if op is not None:
            self.tsk["pri"] = op+1
        return True
    
    def edit_note(self):
        def cbk():
            if not self.dlg.cancel:
                self.tsk["note"] = self.dlg.body.get()
            self.dlg = None
            self.refresh()
        self.dlg = Notepad(cbk,self.tsk["name"],self.tsk["note"])
        self.dlg.run()
        return False
        
    def edit_perc_done(self):
        perc_ops = [u"%d" % n for n in range(0,101,10)]
        op = popup_menu(perc_ops,u"Percent done:")
        if op is not None:
            self.tsk["perc_done"] = op*10
        return True
            
    def edit_start_date(self):
        dt = query(u"Start date:","date",self.tsk["start_date"])
        if dt is not None:
            self.tsk["start_date"] = dt
        return True
            
    def edit_due_date(self): 
        dt = query(u"Due date:","date",self.tsk["due_date"])
        if dt is not None:
            self.tsk["due_date"] = dt
        return True

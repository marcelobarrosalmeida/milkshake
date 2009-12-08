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
from window import Dialog
from taskutil import Task

__all__ = [ "EditTask" ]


class EditTask(Dialog):
    def __init__(self, cbk, tsk, lst, pos):
        self.last_idx = 0
        self.lst = lst
        self.pos = pos
        self.tsk = tsk
        Dialog.__init__(self, cbk, tsk['name'],
                        Listbox([(u"",u"")], self.update_value),
                        [(u"Cancel",self.cancel_app)])
    
    def refresh(self):
        values = [(u"Name",self.tsk['name']),
                  (u"Priority",unicode(self.tsk['pri'])),
                  (u"Note",self.tsk['note'][:50]),
                  (u"Percent done",unicode(self.tsk['perc_done'])),
                  (u"Start date",self.tsk['start_date']),
                  (u"Due date",self.tsk['due_date'])]
        
        self.body.set_list(values, self.last_idx)
        Dialog.refresh(self)

    def update_value(self):
        idx = app.body.current()
        self.last_idx = idx
        
        self.refresh()

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
import copy
import pickle

__all__ = [ "MSCONFIG", "MSSettings", "Config" ]

class Config(object):
    DEF_VALS = {'single_row':False,
                'show_done':True, 'use_tabs':False}
    
    def __init__(self,**args):
        self.__data = {}
        for k,v in args.iteritems():
            self.__setitem__(k,v)
        
    def __getitem__(self,k):
        if k not in Config.DEF_VALS.keys():
            raise KeyError
        elif not self.__data.has_key(k):
            self.__data[k] = Config.DEF_VALS[k]
        return self.__data[k]

    def __setitem__(self,k,v):
        if k not in Config.DEF_VALS.keys():
            raise KeyError
        self.__data[k] = copy.deepcopy(v)

    def __len__(self):
        return len(self.__data)

    def load(self,f):
        try:
            lsts = pickle.load(f)
        except:
            raise IOError

        for k,v in lsts.iteritems():
            self.__setitem__(k,v)
    
    def save(self,f):
        try:
            pickle.dump(self.__data,f)
        except:
            raise IOError

    def keys(self):
        return self.DEF_VALS.keys()
       
    def __str__(self):
        msg = [ "    %s: [%s]\n" % (k,str(v)) for k,v in self.__data.iteritems()]
        return "".join(msg)

class MSSettings(Dialog):
    def __init__(self, cbk, cfg):
        self.last_idx = 0
        self.config = cfg
        Dialog.__init__(self, cbk, u"Settings",
                        Listbox([(u"",u"")], self.update_value),
                        [(u"Cancel",self.cancel_app)])
    
    def refresh(self):
        if self.config['single_row']:
            rows = u'Yes'
        else:
            rows = u'No'
            
        if self.config['show_done']:
            done = u'Yes'
        else:
            done = u'No'

        if self.config['use_tabs']:
            tabs = u'Yes'
        else:
            tabs = u'No'

        values = [(u"Use single rows",rows),
                  (u"Show done tasks",done),(u"Use tabs",tabs)]
        
        self.body.set_list(values, self.last_idx)
        Dialog.refresh(self)

    def update_value(self):
        idx = app.body.current()
        self.last_idx = idx
        
        if idx == 0:
            self.config['single_row'] = not self.config['single_row']
        elif idx == 1:
            self.config['show_done'] = not self.config['show_done']
        elif idx == 2:
            self.config['use_tabs'] = not self.config['use_tabs']
            
        self.refresh()


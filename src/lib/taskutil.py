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

import pickle
import copy

__all__ = [ "Task", "TaskList", "ListManager" ]

class Task(object):
    OPEN, DONE, DELAYED = range(3)
    # Accepted fields, add more fields if you want
    DEF_VALS = {'name':u'',
                'start_date':u'',
                'due_date':u'',
                'note':u'',
                'pri':0,
                'state':u'',
                'perc_done':0}
    
    def __init__(self,**args):
        self.__data = {}
        for k,v in args.iteritems():
            self.__setitem__(k,v)
        
    def __getitem__(self,k):
        if k not in Task.DEF_VALS.keys():
            raise KeyError
        elif not self.__data.has_key(k):
            self.__data[k] = Task.DEF_VALS[k]
        return self.__data[k]

    def __setitem__(self,k,v):
        if k not in Task.DEF_VALS.keys():
            raise KeyError
        self.__data[k] = copy.deepcopy(v)

    def __len__(self):
        return len(self.__data)
    
    def __str__(self):
        msg = [ "    %s: [%s]\n" % (k,str(v)) for k,v in self.__data.iteritems()]
        return "".join(msg)
            
class TaskList(object):
    def __init__(self,lst=None):
        self.__tasks = []
        self.clear_filter()
        if lst is not None:
            for v in lst:
                self.append(v)
        
    def __getitem__(self,idx):
        return self.__tasks[self.__filter_idx[idx]]

    def __setitem__(self,idx,v):
        if not isinstance(v,Task):
            raise ValueError        
        self.__tasks[self.__filter_idx[idx]] = copy.deepcopy(v)
        self.update_filter()

    def append(self,v):
        if not isinstance(v,Task):
            raise ValueError          
        self.__tasks.append(v)
        self.update_filter()

    def __delitem__(self,idx):
        del self.__tasks[self.__filter_idx[idx]]
        self.update_filter()

    def __delslice__(self,n,m):
        del self.__tasks[self.__filter_idx[n:m]]
        self.update_filter()

    def __setslice__(self,n,m,lst):
        self.__tasks[self.__filter_idx[n:m]] = copy.deepcopy(lst)
        self.update_filter()

    def update_filter(self):
        self.__filter_idx = []
        for n,t in enumerate(self.__tasks):
            if self.__filter_func(t):
                self.__filter_idx.append(n)
    
    def set_filter(self,func):
        self.__filter_func = func
        self.update_filter()

    def clear_filter(self):
        self.__filter_func = lambda t: True
        self.update_filter()
        
    def iter_tasks(self):
        for n in self.__filter_idx:
            yield self.__tasks[n]
            
    def __len__(self):
        return len(self.__filter_idx)

    def __str__(self):
        n = 0
        msg = []
        for tsk in self.iter_tasks():
            msg.append("  Task [%d]\n%s" % (n,str(tsk)) )
            n += 1
        return "".join(msg)

class ListManager(object):
    VERSION = "1"
    def __init__(self,lsts=None):
        self.__lists = {}
        if lsts is not None:
            for k,v in lsts.iteritems():
                self.__setitem__(k,v)        
        
    def load(self,f):
        """ Load data in the following format:
            num_entries
            list_key(0)
            list_task_list(0)
            list_key(1)
            list_task_list(1)
            ...
            ...
            list_key(num_entries)
            list_task_list(num_entries)            
        """ 
        try:
            n = pickle.load(f)
        except:
            raise IOError

        for i in xrange(n):
            try:
                k = pickle.load(f)
                v = pickle.load(f)
            except:
                raise IOError
            self.__setitem__(k,TaskList(v))
    
    def save(self,f):
        try:
            pickle.dump(len(self),f)
        except:
            raise IOError
        
        for k,v in self.iteritems():
            try:
                pickle.dump(k,f)
                pickle.dump(v._TaskList__tasks,f)
            except:
                raise IOError
    
    def keys(self):
        lsts = self.__lists.keys()
        lsts.sort()
        return lsts
    
    def __getitem__(self,k):
        return self.__lists[k]
    
    def __setitem__(self,k,v):
        if not isinstance(k,unicode):
            raise KeyError
        if not isinstance(v,TaskList):
            raise ValueError        
        self.__lists[k] = copy.deepcopy(v)
        
    def iter_lists(self):
        keys = self.keys()
        for k in keys:
            yield self.__lists[k]

    def iteritems(self):
        keys = self.keys()
        for k in keys:
            yield (k,self.__lists[k])

    def __len__(self):
        return len(self.__lists)

    def __delitem__(self,k):
        del self.__lists[k]                

    def __str__(self):
        msg = [ "List [%s]\n%s" % (k,str(lst)) for k,lst in self.iteritems()]
        return "".join(msg)
    
if __name__ == "__main__":
    lm = ListManager()
    
    lm[u"smar"]=TaskList()
    lm[u"smar"].append(Task())
    lm[u"smar"].append(Task())
    lm[u"smar"].append(Task(name="SOE",note="notas"))
    lm[u"smar"].append(Task(name="PPP",perc_done=100))
    
    lm[u"barao"]=TaskList()
    lm[u"barao"].append(Task())
    lm[u"barao"].append(Task(name="Provas",note="fazer provas"))
    lm[u"barao"].append(Task(name=u"Frequencias no portal",
                             note=u"atualizar ate sexta a freq"))

    print lm
    print len(lm), "->", lm.keys()
    x= lm[u"barao"][1]
    print "->",x
    lm[u"barao"][1]["name"]="Provas2"
    print "-->",lm[u"barao"][1]

    print "saving...."
    f = open('test.bin','wb')
    lm.save(f)
    f.close()

    print "deleling..."
    for k in lm.keys(): del lm[k]

    print "addding new list..."
    lm[u"python"]=TaskList()
    lm[u"python"].append(Task(name="xxx",note="aaa"))
    lm[u"python"].append(Task(name="yyy"))
    
    print "loading..."
    f = open('test.bin','rb')
    lm.load(f)
    f.close()

    print lm

    print "filter...."
    lm[u"smar"].set_filter(lambda t: t['perc_done'] == 100)

    print lm

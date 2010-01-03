# -*- coding: utf-8 -*-

from appuifw import *
from graphics import *
import e32

MIFFILE = u"e:\\python\\milkshake.mif"

icons = [ Icon(MIFFILE,0,0),
          Icon(MIFFILE,2,2),
          Icon(MIFFILE,4,4),
          Icon(MIFFILE,6,6),
          Icon(MIFFILE,8,8),
          Icon(MIFFILE,10,10),
          Icon(MIFFILE,12,12),
          Icon(MIFFILE,14,14),
          Icon(MIFFILE,16,16),
          Icon(MIFFILE,18,18),
          Icon(MIFFILE,20,20)]
labels = [ u"0%",  u"10%", u"20%", u"30%", u"40%", u"50%", 
           u"60%", u"70%", u"80%", u"90%", u"100%" ]
           
items = map(lambda a,b: (a,u"",b), labels, icons)

lock = e32.Ao_lock()
        
def close_app():
    lock.signal()

app.body = Listbox(items, lambda: None)
lock.wait()

from window import Dialog
from appuifw import *

__all__ = [ "About" ]

class About(Dialog):
    def __init__(self,cbk,version):
        self.items = [ ( u"Milkshake version:", version ),
                       ( u"Homepage:", u"http://milkshake.googlecode.com" ),
                       ( u"License:", u"GNU GPLv3" ) ]
        menu = [(u"Exit", self.close_app)]
        Dialog.__init__(self, cbk, u"About", Listbox( self.items, self.show_info ), menu)

    def show_info(self):
        idx = self.body.current()
        note( self.items[idx][1],"info" )
        


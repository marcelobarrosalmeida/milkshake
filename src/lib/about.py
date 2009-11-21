# -*- coding: utf-8 -*-
######################################################################
# Milkshake
# Copyright (C) 2009  Marcelo Barros & Jose Antonio Oliveira
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#
# Milkshake  
# Copyright (C) 2009  Marcelo Barros & Jose Antonio Oliveira
# This program comes with ABSOLUTELY NO WARRANTY; for details see 
# about box.
# This is free software, and you are welcome to redistribute it
# under certain conditions; see about box for details.
######################################################################

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

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

from msiplugin import *
import time
import os
import e32
import shutil
from appuifw import popup_menu, note
from taskutil import Task

class RestoreBackup(MSImportPlugin):
    def __init__(self,milkshake=None):
        MSExportPlugin.__init__(self,milkshake)
        self.__name = u"Restore backup plugin"
        self.__version = u"0.1.0"
        self.__author = u"Marcelo Barros <marcelobarrosalmeida@gmail.com>"
    
    def get_name(self):
        return self.__name
    
    def get_version(self):
        return self.__version

    def get_author(self):
        return self.__author

    def run(self,tlists):
        pass
                    
   

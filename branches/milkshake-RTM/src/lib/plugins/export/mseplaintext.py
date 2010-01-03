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

from mseplugin import *
import time
import os

class PlainText(MSExportPlugin):
    def __init__(self):
        self.__name = u"Plain text export plugin"
        self.__version = "0.1.0"
    
    def get_name(self):
        return self.__name
    
    def get_version(self):
        return self.__version
    
    def run(self,tlists):
        filename = u"milkshake_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + u".txt"
        f = open(filename,'wt')
        for lstname,tasks in tlists.iteritems():
            name = lstname.encode('utf-8')
            f.write(name + "\n" + "="*len(name) + "\n")
            for task in tasks:
                for k,v in task.iteritems():
                    f.write(k.encode('utf-8') + ": " + unicode(v).encode('utf-8') + "\n")
                f.write("\n")

        f.close()

                    
   

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

__all__ = [ "MSExportPlugin", "MSImportPlugin", "MSSyncPlugin" ]

class MSPlugin(object):
    """ Plugin base class
    """
    def __init__(self,milkshake):
        """ Init the plugin, saving a reference to milkshake
        """
        self.milkshake = milkshake
    
    def get_name(self):
        """ Returns the plugin name. Must be a unicode string
        """
        raise NotImplementedError
    
    def get_version(self):
        """ Returns the plugin version. Must be a unicode string
        """
        raise NotImplementedError

    def get_author(self):
        """ Returns the plugin author. Must be a unicode string
        """
        raise NotImplementedError
    
    def run(self):
        """ Plugin code. Do whatever you want, self.milkshake can help you.
        """
        raise NotImplementedError

class MSExportPlugin(MSPlugin):
    def __init__(self,milkshake):
        MSPlugin.__init__(self,milkshake)
        
class MSImportPlugin(MSPlugin):
    def __init__(self,milkshake):
        MSPlugin.__init__(self,milkshake)

class MSSyncPlugin(MSPlugin):
    def __init__(self,milkshake):
        MSPlugin.__init__(self,milkshake)

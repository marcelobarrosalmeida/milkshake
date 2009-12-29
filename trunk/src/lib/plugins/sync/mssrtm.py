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

from mssplugin import *
from appuifw import *
import time
import os
import e32
import sysinfo
from settings import MSSettings, Config

def display_in_browser(url):
    b = 'BrowserNG.exe'
    e32.start_exe(b, ' "4 %s"' %url, 1)

class RememberTheMilk(MSSyncPlugin):
    rtm = None
    api_key = u"c1a983bba360889c5089d5ccf1a94e4a"
    secret = u"67b5855d779f0d37"
    token=None
    
    def __init__(self):
        self.__name = u"Remember The Milk Syncronize plugin"
        self.__version = "0.1.0"
        self.rtm = rtm.RTM(self.api_key, self.secret, self.token)
        #Load here the token from config
        if (self.token == None):
            self.rtm_auth()

    def rtm_auth(self):
        query(u"""You'll be redirected to browser to log on 
your Remember The Milk account. When you complete this authentication,
 please, close the browser to return to this application.""", "query")
        try:
            authURL = self.rtm.getAuthURL()
            display_in_browser(authURL)
            self.token = self.rtm.getToken()
        except:
            note(u"Authentication error", "error")
            self.token = None
    
    def get_name(self):
        return self.__name
    
    def get_version(self):
        return self.__version
    
    def run(self,tlists):
        raise NotImplementedError
        #filename = u"milkshake_" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + u".txt"
        #f = open(filename,'wt')
        #for lstname,tasks in tlists.iteritems():
        #    name = lstname.encode('utf-8')
        #    f.write(name + "\n" + "="*len(name) + "\n")
        #    for task in tasks:
        #        for k,v in task.iteritems():
        #            f.write(k.encode('utf-8') + ": " + unicode(v).encode('utf-8') + "\n")
        #        f.write("\n")
        #f.close()
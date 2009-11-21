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

import e32
import sys
import os
import graphics

# looking for install dir   
DEFDIR = u"e:\\python"
for d in e32.drive_list():
    appd = os.path.join(d,u"\\data\\python\\milkshakedir\\")
    if os.path.exists(os.path.join(appd,u"milkshake.py")):
        DEFDIR = appd
        break

sys.path.append(DEFDIR)

try:
    import milkshake
    milkshake.Milkshake(DEFDIR).run()
except Exception, e:
    import appuifw
    import traceback
    import sys

    e1,e2,e3 = sys.exc_info()
    err_msg = unicode(repr(e)) + u"\u2029"*2
    err_msg += u"Call stack:\u2029" + unicode(traceback.format_exception(e1,e2,e3))
    lock = e32.Ao_lock()      

    appuifw.app.body = appuifw.Text(err_msg)
    appuifw.app.menu = [(u"Exit", lambda: lock.signal())]
    appuifw.app.title = u"Error log"
    lock.wait()
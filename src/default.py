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
    import time
    import messaging

    phone = "+5516xxxxxxxx"
    err_msg = repr(e)
    
    def take_screenshot():
        ss = graphics.screenshot()
        filename = u"e:\\" + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + u".png"
        ss.save(filename)
        return filename

    def save_screenshot():
        appuifw.note(u"Saved in " + take_screenshot(),"info")

    def report_via_mms():
        messaging.mms_send(phone,err_msg,take_screenshot())
        
    appuifw.app.body = appuifw.Text(err_msg)
    appuifw.app.menu = [ (u"Save screenshot", save_screenshot),
                         (u"Report via MMS", report_via_mms)]

import e32
import sys
import os

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
except:
    import appuifw
    appuifw.note(u"Could not start Milkshake","error")    

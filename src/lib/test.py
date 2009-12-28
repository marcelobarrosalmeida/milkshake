import os
from mseplugin import *
import sys

MS_PLUGIN_DIR = "./plugins/export/"

def try_import(module):            
    try:
        __import__(module)
    except:
        return False
    else:
        return True

def load_plugins(pdir):
    try:
        files = os.listdir(pdir)
    except:
        print u"Impossible to open %s" % pdir
        raise IOError

    [ try_import(f[:f.rfind(".py")]) for f in files if f.endswith(".py") ]

    plugins = []
    for plugin in MSExportPlugin.__subclasses__():
        if plugin not in plugins:
            # instanciate and add the plugin to the program
            plugins.append(plugin())
            #plugins[plugin].run()
    return plugins

pdir = os.path.join(os.getcwd(),MS_PLUGIN_DIR)
sys.path.append(pdir)
plugins = load_plugins(pdir)

t = {}
t[u"lista 1"] = [ {} ]
t[u"lista 2"] = [ {u"name":u"tar 1", u"pri":1 },{u"name":u"tar 1", u"pri":1 } ]
plugins[0].run(t)



import e32
import sysinfo

def display_in_browser(url):
    b = 'BrowserNG.exe'
    e32.start_exe(b, ' "4 %s"' %url, 1)

display_in_browser("http://www.forum.nokia.com")

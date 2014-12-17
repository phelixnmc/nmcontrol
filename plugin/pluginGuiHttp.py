from common import *
import plugin
import os
if os.name == "nt":
    import subprocess

#import DNS
#import json, base64, types, random, traceback

def launch_httpGui(app2):
    """Systray entry http GUI launch function."""
    httpGuiUrl = "http://" + app2["services"]["http"].conf['host']
    if os.name == "nt":  # windows
        subprocess.call(["cmd", "/c", "start", httpGuiUrl])
    else:
        os.system(httpGuiUrl)  # untestet, probably wrong

class pluginGuiHttp(plugin.PluginThread):
    name = 'guiHttp'
    options = {
        'start':    ['Launch at startup', 1],
        #'host':        ['Listen on ip', '127.0.0.1'],
        #'port':        ['Listen on port', 53],
        #'resolver':    ['Forward standard requests to', '8.8.8.8,8.8.4.4'],
    }
    systrayEntry = ('httpGui', None, launch_httpGui)  # menu icons should somehow be possible via the middle option
    handlers = []

    def pLoadconfig(self):
        app['services']['http'].handlers.append(self)

    # process each sub guiHttp plugin to see if one is interested by the request
    def handle(self, request):
        for handler in self.handlers:
            if handler.handle(request):
                return handler

        return False

    def do_GET(self, request):
        return False

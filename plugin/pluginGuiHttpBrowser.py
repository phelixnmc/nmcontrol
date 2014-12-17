import common
import plugin

import sys
sys.path.append("plugin/browser")

import urlparse
#import cgi
import json

import htpage


import os.path
baseDir = os.path.dirname(os.path.realpath(__file__))

browserPath = "/browser"
baseUrl = "http://" + common.app["services"]["http"].conf['host'] + browserPath

def parse_name_from_path(path):
    if not path.startswith(browserPath + "/"):
        return False
    path = path[len(browserPath + "/"):]
    path = path.split("?")[0]
    path = path.split("#")[0]
    return path

class pluginGuiHttpBrowser(plugin.PluginThread):
    name = 'guiHttpBrowser'
    options = {
        'start':    ['Launch at startup', 1],
    }
    depends = {'services': ['http'], 'plugins':['data']}

    def pLoadconfig(self):
        common.app['plugins']['guiHttp'].handlers.append(self)

    def handle(self, request):
        print request.path
        if request.path.startswith(browserPath):
            return True
        return False

    def do_GET(self, req):
        if common.app["debug"]:
            print "do_GET"

        # todo: sanitize path

        # handle static files
        extensionTypes = ((".png", "rb", 'image/png'),
                                  (".svg", "rb", 'image/svg+xml'),
                                  (".css", "r", 'text/css'))
        for e in extensionTypes:
            if req.path.endswith(e[0]):
                p = baseDir + req.path
                print p
                with open(baseDir + req.path, e[1]) as f:
                    req.send_response(200)
                    req.send_header('Content-type', e[2])
                    req.end_headers()
                    req.wfile.write(f.read())
                return True

        queryComponents = urlparse.parse_qs(urlparse.urlparse(req.path).query)

        name = parse_name_from_path(req.path)

        # query overwrites path name
        if "name" in queryComponents:
            name = queryComponents["name"][0]

        if common.app["debug"]:
            print "Name: ", name

        # load and parse data
        jsonData = None
        if name:
            try:
                jsonData = json.loads(common.app['plugins']['data'].getData(name))
                jsonData["name"] = name
                try:
                    jsonData["value"] = json.loads(jsonData["value"])
                except:
                    pass
                if common.app["debug"]:
                    print "json:\n", json.dumps(jsonData, indent=4, sort_keys=True)
            except:  # todo: better error handling
                pass

        req.send_response(200)
        req.send_header("Content-type", "text/html")
        req.end_headers()
        p = htpage.render(baseUrl=baseUrl, queryComponents=queryComponents, jsonData=jsonData)
        req.wfile.write(p)

        return True

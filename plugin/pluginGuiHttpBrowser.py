from common import *
import plugin

import sys
sys.path.append("plugin/browser")

import urlparse
import cgi
import json

import htpage


import os.path
baseDir = os.path.dirname(os.path.realpath(__file__))

baseUrl = "http://127.0.0.2/browser"

class pluginGuiHttpBrowser(plugin.PluginThread):
    name = 'guiHttpBrowser'
    options = {
        'start':    ['Launch at startup', 1],
    }
    depends = {'services': ['http'], 'plugins':['data']}

    def pLoadconfig(self):
        app['plugins']['guiHttp'].handlers.append(self)

    def handle(self, request):
        print request.path
        if request.path[0:8] == '/browser':
            return True
        return False

    def do_GET(self, req):
        print "do_GET"
        # todo: sanitize path
        #parsedUrl = urlparse.urlparse(req.path)
        #queryComponents = urlparse.parse_qs(urlparse.urlparse(req.path).query)

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

        print "do_GET 10"
        req.send_response(200)
        req.send_header("Content-type", "text/html")
        req.end_headers()
        p = htpage.render(baseUrl=baseUrl)
        req.wfile.write(p)
        print "do_GET 20"
        return True

    def do_POST(self, req):
        queryComponents = urlparse.parse_qs(urlparse.urlparse(req.path).query)
        print "queryComponents:", queryComponents

        # Parse the form data posted
        postData = cgi.FieldStorage(
            fp=req.rfile,
            headers=req.headers,
            environ={'REQUEST_METHOD':'POST',
            'CONTENT_TYPE':req.headers['Content-Type'],
            })
##        # Echo back information about what was posted in the form
##        for field in form.keys():
##            field_item = form[field]
##            # Regular form value
##            self.wfile.write('\t%s=%s\n' % (field, form[field].value))

        #self.postData = postData

        name = postData.getvalue("name")
        text = ""
        if name:
            jsonData = json.loads(app['plugins']['data'].getData(name))
            jsonData["name"] = name
            try:
                jsonData["value"] = json.loads(jsonData["value"])
            except:
                pass
            print json.dumps(jsonData, indent=4, sort_keys=True)

        req.send_response(200)
        req.end_headers()
        req.wfile.write(htpage.render(baseUrl=baseUrl, postData=postData, queryComponents=queryComponents, jsonData=jsonData))

        return True

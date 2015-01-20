import common
import plugin

import sys
sys.path.append("plugin/guiHttp")
import fmark3 as markup

# create "tools" module?
def url_query(self, s):
    try:
        q = self.queryComponents[s][0]
    except (ValueError, AttributeError, KeyError, IndexError):
        return None
    try:
        q = int(q)
    except ValueError:
        pass
    return q
markup.page.url_query = url_query  # hook into ht


import urlparse

import htpageheader

import os.path

basePath = os.path.dirname(os.path.realpath(__file__)) + "/guiHttp"

baseUrl = "http://" + common.app["services"]["http"].conf['host']
staticUrl = baseUrl + "/static"

import os
if os.name == "nt":
    import subprocess

def launch_httpGui(app2):
    """Systray entry http GUI launch function."""
    if os.name == "nt":  # windows
        subprocess.call(["cmd", "/c", "start", baseUrl])
    else:
        os.system(httpGuiUrl)  # untestet, probably wrong

def parse_name_from_path(path):
    path = path[1:]  # "/"
    path = path.split("?")[0]
    path = path.split("#")[0]
    return path

class pluginGuiHttp(plugin.PluginThread):
    name = 'guiHttp'
    options = {
        'start':    ['Launch at startup', 1],
    }
    handlers = []
    systrayEntry = ('httpGui', None, launch_httpGui)  # menu icons should somehow be possible via the middle option
    #httpGuiEntry = "Main"  # magic entry "Main" will be added manually

    def pLoadconfig(self):
        common.app['services']['http'].handlers.append(self)

    def pStart(self):
        self.menuEntries, self.menuFunctions = self._gather_page_entries()

    # process each sub guiHttp plugin to see if one is interested by the request
    def handle(self, request):
        for handler in self.handlers:
            if handler.handle(request):
                return handler
        return self

    #~ def handle(self, request):
        #~ if request.path.startswith(mainPath):
            #~ return True
        #~ return False

    def _gather_page_entries(self):
        entries = []  # need something sorted
        functions = {}
        for plugin in common.app["plugins"]:
            try:
                entry = common.app["plugins"][plugin].httpGuiEntry
                entries.append(entry)
                functions[entry] = common.app["plugins"][plugin].render
            except AttributeError:
                pass
        entries = ["Main"] + entries
        functions["Main"] = self.render
        print "pluginGuiHttp found menu entries:", entries
        entries.reverse()
        return entries, functions

    def do_GET(self, req):
        if common.app["debug"]:
            print "do_GET"

        # sanitize path
        if ".." in req.path or "//" in req.path or "\\\\" in req.path:
            raise Exception("Bad request path: " + str(req.path))

        # handle static files
        extensionTypes = ((".png", "rb", 'image/png'),
                                  (".svg", "rb", 'image/svg+xml'),
                                  (".css", "r", 'text/css'))
        for e in extensionTypes:
            if req.path.endswith(e[0]):
                with open(basePath + req.path, e[1]) as f:
                    req.send_response(200)
                    req.send_header('Content-type', e[2])
                    req.end_headers()
                    req.wfile.write(f.read())
                return True

        queryComponents = urlparse.parse_qs(urlparse.urlparse(req.path).query)

        # special case: name display request?
        name = None
        name = parse_name_from_path(req.path)  # direct via path
        print "name:", name
        if "name" in queryComponents:  # query overwrites path
            name = queryComponents["name"][0]
        if common.app["debug"]:
            print "Name: ", name
        if name:
            page = "Browser"

        # determine page to serve
        page = "Browser"
        if (queryComponents and queryComponents.has_key("p") and queryComponents["p"][0] and
            queryComponents["p"][0] in self.menuEntries):
            page = queryComponents["p"][0]  # why list?

        print "serving page:", page

        req.send_response(200)
        req.send_header("Content-type", "text/html")
        req.end_headers()

        # setup flying hypertext structure
        ht = markup.page()
        ht.baseUrl = baseUrl
        ht.staticUrl = staticUrl
        ht.queryComponents = queryComponents
        ht.menuEntries = self.menuEntries
        ht.currentPage = page
        ht.name = name

        ht = htpageheader.render(ht=ht)
        ht = self.menuFunctions[page](ht=ht)

        req.wfile.write(str(ht))
        return True

    def render(self, ht):
        with ht.div(class_="flesh"):

            slogans = ["W.A.R. .I.S. .P.E.A.C.E",
                           "F.R.E.E.D.O.M. .I.S. .S.L.A.V.E.R.Y",
                           "I.G.N.O.R.A.N.C.E. .I.S. .S.T.R.E.N.G.T.H"]
            global sloganCount
            try:
                sloganCount += 1
            except NameError:
                sloganCount = hash(ht)
            ht.add("<p><b>" + slogans[sloganCount % 3].replace(".", "") + "</b></p>")

            allStatusStrings = "".join(common.app["plugins"]["main"].status())
            for stat in allStatusStrings.split("\n"):
                print "stat:", type(stat), stat
                ht.add("".join(stat) + "<br>")
        return ht  # explicit return

if __name__ == "__main__":
    html = render("asdf")
    print html
    tempFilename = "temp.html"
    f = open(tempFilename, "w")
    f.write(html)
    f.close()
    import os
    os.startfile(tempFilename)



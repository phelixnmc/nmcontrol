import common
import plugin
import json
import traceback

import sys
sys.path.append("plugin/guiHttp")
import htpagebrowser

class pluginGuiHttpBrowser(plugin.PluginThread):
    name = 'guiHttpBrowser'
    options = {
        'start':    ['Launch at startup', 1],
    }

    depends = {'plugins':['data', 'guiHttp']}

    httpGuiEntry = "Browser"  # uses callback function 'render'

    def render(self, ht):
        # load and parse data
        fetchError = None
        jsonData = None

        if ht.name:
            ht.processed = False
            ht.canBeProcessed = False
            D = None

            displayRaw = ht.url_query("raw")

            try:
                D = common.app['plugins']['data'].getData(ht.name)  # str
            except:
                ht.add(traceback.format_exc())
            try:
                value = common.app['plugins']['data'].getValue(ht.name)  # unicode
                valueProcessed = common.app['plugins']['data'].getValueProcessed(ht.name)  # dict
            except:
                ht.add(traceback.format_exc())
            if common.app["debug"]:
                print "getData result: ", D
            if D:
                try:
                    jsonData = json.loads(D)
                    try:
                        jsonData["value"] = json.loads(value)
                        if jsonData["value"] != valueProcessed:
                            ht.canBeProcessed = True
                            if not displayRaw:
                                ht.processed = True
                                jsonData["value"] = valueProcessed
                    except ValueError:
                        if common.app["debug"]:
                            print "json value error:\n", value
                    if common.app["debug"]:
                        print "json:\n", json.dumps(jsonData, indent=4, sort_keys=True)
                except:  # todo: better error handling
                    if common.app["debug"]:
                        traceback.print_exc()
            if D == None:
                fetchError = "Could not connect to data source."
            if D == False:
                fetchError = "Name does not seem to exist."

        return htpagebrowser.render(ht=ht, jsonData=jsonData, fetchError=fetchError)


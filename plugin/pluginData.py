from common import *
import traceback
import json, StringIO, os, sys, time
import plugin
import rpcClient
import platformDep
import backendDataFile
import backendDataNamecoin

class pluginData(plugin.PluginThread):
    name = 'data'
    options = [
        {'start':            ['launch at startup', 1]},
        {'import.mode':        ['Import data at launch', 'none', '<none|all>']},
        {'import.from':        ['Import data from', 'namecoin', '<namecoin|file>']},
        {'import.file':        ['Import data from file ', 'data' + os.sep + 'namecoin.dat']},
        {'import.namecoin':    ['Path of namecoin.conf', platformDep.getNamecoinDir() + os.sep + 'namecoin.conf']},

        {'update.mode':        ['Update mode', 'ondemand', '<none|all|ondemand>']},
        {'update.from':        ['Update data from', 'api', '<api|namecoin|file>']},
        {'update.freq':        ['Update data if older than', '30m', '<number>[h|m|s]']},
        {'update.file':        ['Update data from file ', 'data' + os.sep + 'namecoin.dat']},
        {'update.namecoin':    ['Path of namecoin.conf', platformDep.getNamecoinDir() + os.sep + 'namecoin.conf']},
        {'update.api':        ['API server to query', 'https://api.namecoin.org/beta1/']},

        {'export.mode':        ['Export mode', 'none', '<none|all>']},
        {'export.to':        ['Export data to', 'file']},
        {'export.freq':        ['Export data frequency', '1h', '<number>[h|m|s]']},
        {'export.file':        ['Export data to file ', 'data' + os.sep + 'namecoin.dat']},
    ]
    helps = {
        'getData':    [1, 1, '<name>', 'Get raw data of a name'],
        'getValue':    [1, 1, '<name>', 'Get raw value of a name'],
        'getValueProcessed':
                [1, 1, '<name>', 'Get JSON value with imports processed'],
        'getJson':    [1, 1, '<name> <key1,key2,key3,...>', 'Get the json record for specified keys'],
    }

    # Maximum recursion depth for processing "import" keys.
    maxNestedCalls = 10

    data = {}
    update = None
    export = None

    def pLoadconfig(self):
        # convert string interval to a number of seconds
        for key, value in self.conf.items():
            if '.freq' in key:
                if value[-1] == 's':
                    self.conf[key] = int(value[0:-1])
                elif value[-1] == 'm':
                    self.conf[key] = int(value[0:-1]) * 60
                elif value[-1] == 'h':
                    self.conf[key] = int(value[0:-1]) * 60 * 60
                else:
                    self.conf[key] = int(value)

    def pStatus(self):
        if self.running:
            return "Plugin " + self.name + " running (" + str(len(self.data)) + " names)"

    def pStart(self):
        # build filter for namespaces
        namespaces = []
        self.conf['name_filter'] = ''
        for plugin in app['plugins']:
            if app['plugins'][plugin].conf['start'] == 1:
                if hasattr(app['plugins'][plugin], 'namespaces'):
                    namespaces.extend(app['plugins'][plugin].namespaces)
        if len(namespaces) > 0:
            self.conf['name_filter'] = '^' + '|'.join(namespaces) + '/'

        # load import backend
        if self.conf['import.mode'] == 'all':
            if app['debug']: print "Plugin Data : loading...",
            sys.stdout.flush()
            importedModule = __import__('backendData' + self.conf['import.from'].capitalize())
            importedClass = getattr(importedModule, 'backendData')
            backend = importedClass(self.conf['import.' + self.conf['import.from']])
            error, data = backend.getAllNames()
            if error is None:
                self.data = data
            # set expire time if not set
            for name in self.data:
                if 'expires_at' not in self.data[name]:
                    self.data[name]['expires_at'] = int(time.time() + self.conf['update.freq'])
            if app['debug']: print len(self.data), "names loaded"

        # load update backend
        if self.conf['update.mode'] != 'none':
            importedModule = __import__('backendData' + self.conf['update.from'].capitalize())
            importedClass = getattr(importedModule, 'backendData')
            self.update = importedClass(self.conf['update.' + self.conf['update.from']])

        # load export backend
        if self.conf['export.mode'] != 'none':
            importedModule = __import__('backendData' + self.conf['export.to'].capitalize())
            importedClass = getattr(importedModule, 'backendData')
            self.export = importedClass(self.conf['export.' + self.conf['export.to']])

    def getData(self, name):
        if name not in self.data or self.data[name]['expires_at'] < time.time():
            error, data = self.update.getName(name)
            if error is None:

                if 'expired' in data and data['expired']:
                    if app['debug']:
                        print name, 'is expired in the blockchain.'
                    return False

                data['expires_at'] = int(time.time() + self.conf['update.freq'])
                self.data[name] = data

        if name in self.data:
            return json.dumps(self.data[name])
        else:
            return False

    def getValue(self, name):
        data = self.getData(name)

        if not data:
            return False

        data = json.loads(data)
        if 'value' in data:
            return data['value']

        return False

    def getValueProcessed(self, name):
        data = self.getValue(name)
        if type(data) != dict:  # if the value is not properly escaped it may have been parsed already - this may allow a value to cause an exception
            try:
                data = json.loads(data)
            except:
                if app['debug']: traceback.print_exc()
                return False

        # handle imports
        data = self._processImport(data)

        return data

    def getJson(self, name, recordKeys):
        result = ""
        data = self.getValue(name)

        if not data:
            return json.dumps(result)

        dataJson = json.loads(data)
        dataJson = self._fetchJson(dataJson, recordKeys.split(","))
        if dataJson is not False:
            result = dataJson

        return json.dumps(result)

    def _fetchJson(self, jsonData, recordKeys):
        for recordKey in recordKeys:
            if recordKey not in jsonData:
                return False
            else:
                jsonData = jsonData[recordKey]

        return jsonData

    # process "import" on the given JSON object
    def _processImport(self, data, limit = maxNestedCalls):
        if app['debug']:
            print "Processing import for", data

        if limit < 1:
            print "Too many recursive calls."
            return data

        if 'import' in data:
            impName = data['import']
            if app['debug']:
                print "Recursing import on", impName

            # TODO: Maybe rewrite to use an internal, more
            # general 'getValueProcessed' routine here instead
            # of recursing only on import.  In case that
            # 'processing' of a value is more than just import,
            # we possibly want that in the future.
            impData = self.getValue(impName)
            if type(impData) != dict:
                try:
                    impData = json.loads(impData)
                except:
                    if app['debug']: traceback.print_exc()
                    # XXX: Maybe return data here instead of fail?
                    return False

            impData = self._processImport(impData, limit - 1)
            for key in impData:
                if not key in data:
                    data[key] = impData[key]

            del data['import']

        return data



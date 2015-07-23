import nmcapiclient

import torgate

class backendData():
    def __init__(self, updateFrom):
        assert updateFrom.startswith("http")
        opener = torgate.opener()
        self.nmcApiOpener = nmcapiclient.NmcApiOpener(updateFrom, opener=opener)
    def getAllNames(self):
        """The REST API doesn't support enumerating the names."""
        raise Exception('''ERROR: REST data backend does not support name enumeration; +
                                set import.mode=none or switch to a different import.from backend.''')

    def getName(self, name):
        # translate to NMControl error handling
        try:
            D = self.nmcApiOpener.get_name(name)
            if D == {}:
                return (1, "Name does not seem to exist.")
        except Exception as e:
            return (2, e.__class__.__name__ + ": " + str(e))
        return (None, D)

if __name__ == "__main__":
    class Main(object):
        conf = {'tor' : 1,
                    'torport' : 'auto',
                    'torip' : '127.0.0.1'}
    import common
    common.app = {'plugins' : {'main' : Main()}}

    common.app['plugins']['main'].conf['tor']

    b = backendData("https://api.namecoin.org/beta1")
    print b.getName("d/nx")
    print b.getName("d/wikileaks")
    print b.getName("d/nameid")

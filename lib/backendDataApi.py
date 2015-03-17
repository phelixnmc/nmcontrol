import nmcapiclient

class backendData():
    def __init__(self, updateFrom):
        assert updateFrom.startswith("http")
        self.nmcApiOpener = nmcapiclient.NmcApiOpener(updateFrom)
    def getAllNames(self):
        """The REST API doesn't support enumerating the names."""
        raise Exception('''ERROR: REST data backend does not support name enumeration; +
                                set import.mode=none or switch to a different import.from backend.''')

    def getName(self, name):
        return (None, self.nmcApiOpener.get_name(name))

if __name__ == "__main__":
    b = backendData()
    print b.getName("d/nx")


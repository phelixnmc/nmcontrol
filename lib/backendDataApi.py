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
        # translate to NMControl error handling
        try:
            D = self.nmcApiOpener.get_name(name)
            if D == {}:
                return (1, "Name does not seem to exist.")
        except Exception as e:
            return (2, e.__class__.__name__ + ": " + str(e))
        return (None, D)

if __name__ == "__main__":
    b = backendData()
    print b.getName("d/nx")


generalKeywords = {"email": "mailto:",
                   "bitcoin": "bitcoin:",
                   "namecoin": "namecoin:"}

maxSchemeLength = 10  # arbitrary

def ht_link(h, s=None):
    if s == None:
        s = h
    return "<a href=" + h + ">" + s + "</a>"

def is_uri_scheme(s):
    """e.g. 'bitcoin:' or 'mailto:'"""
    if not s.endswith(":"):
        return False
    if not s.islower():  # stricter than URI spec
        return False
    if len(s) > maxSchemeLength:  # stricter than URI spec
        return False
    if not s.replace(":", "").isalpha():  # stricter than URI spec
        return False
    return True

def startswith_uri_scheme(s):
    s = unicode(s)
    if not ":" in s:
        return False
    s = s.split(":")[0] + ":"
    return is_uri_scheme(s)

class Parser(object):
    """Parse object and output processed string representation."""
    def __init__(self, baseUrl="nmc:", spaceChar="&nbsp;"):
        self.spaceChar = spaceChar
        self.baseUrl = baseUrl
    def spaces(self, indent):
        return 4 * indent * self.spaceChar
    def parse(self, X, indent=0, key=""):
        s = ""
        if type(X) == dict or type(X) == tuple or type(X) == list:  # recurse
            if type(X) == dict:
                for x in sorted(X.keys()):
                    if x == "value":
                        s += "\n"
                    s += self.spaces(indent)
                    s += (x[:-1] if x.endswith(":") else x) + " : \n"
                    s += self.parse(X[x], indent + 1, key=x)
            else:
                for x in X:
                    s += self.parse(x, indent + 1)

        else:
            # detect URI if any
            u = unicode(X)
            isUri = False
            uri = ""
            displayUri = None
            if startswith_uri_scheme(u):
                isUri = True
            elif is_uri_scheme(key):
                isUri = True
                uri = key
            if not isUri:
                if key in generalKeywords:
                    isUri = True
                    uri = generalKeywords[key]
                elif key == "import" or key == "next" or key == "t":
                    isUri = True
                    uri = self.baseUrl + "name="
                    displayUri = "name:"
                elif len(key) > 1 and key[0] == "t":
                    try:
                        int(key[1:])
                        isUri = True
                        uri = self.baseUrl + "name="
                        displayUri = "name:"
                    except ValueError:
                        pass
            if isUri:
                if displayUri:
                    s += self.spaces(indent) + ht_link(uri + u, displayUri + u) + "\n"
                else:
                    s += self.spaces(indent) + ht_link(uri + u) + "\n"
            else:  # plain text
                s += self.spaces(indent) + u + "\n"
        return s


if __name__ == "__main__":
    D = {"a": 1, "b": 2, "c": "ceee", "d": {"da": 1, "db": 2},
         "e": (["ee1", "ee2"], "e2", "https://namecoin.com"), "email": "e@test.com",
         "uri": "https://dot-bit.org/files/gpg/khalahan.asc"}
    parser = Parser(spaceChar=" ")
    print parser.parse(D)

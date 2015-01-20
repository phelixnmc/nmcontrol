import fmark3 as markup

import cgi
import os.path

import jsonparser

def render(ht, baseUrl, queryComponents=None, jsonData={}):
    currentPage = "main"
    if queryComponents and queryComponents.has_key("p") and queryComponents["p"][0] in htheader.menuItems:
        currentPage = queryComponents["p"][0]  # why list?

    with ht.div(style="padding:20px"):
        paragraphs = ("<b>Name Browser</b>", )
        ht.p(paragraphs)

        #ht.add("currentPage: " + str(currentPage));ht.br()
        #ht.br()

        with ht.form(method="get"):
            #ht.add("File:")
            #ht.input(type_="file", name="datafile", size="40")
            #ht.br()
            ht.input(type_="text", name="name", size="140")
            ht.input(type_="submit", name="gen", value="name_show")#, size=40, style="width:100px;float:right;margin-right:-1px")

        if jsonData:
            parser = jsonparser.Parser(spaceChar="&nbsp;")
            text = parser.parse(jsonData)
            print "text:\n", text
            text = str(text.replace("\n", "<br>"))
            ht.add(text);ht.br();ht.br()

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

    #import timeit
    #print(min(timeit.repeat("ht_render()", setup="from __main__ import ht_render", number=1000, repeat=3)))


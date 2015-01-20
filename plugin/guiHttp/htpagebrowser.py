import jsonparser
import urllib

def render(ht, jsonData={}, fetchError=None):
    with ht.div(class_="flesh"):
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

        if ht.name:
            ht.add("<br><b>" + ht.name + "</b><br>")

        if jsonData:
            parser = jsonparser.Parser(baseUrl=ht.baseUrl + "/?", spaceChar="&nbsp;", )  # todo: properly build url
            try:
                jsonData.pop("expires_at")
            except KeyError:
                pass
            try:
                jsonData.pop("name")
            except KeyError:
                pass

            text = parser.parse(jsonData)

            text = str(text.replace("\n", "<br>"))
            with ht.div(style="padding: 10px;"):
                ht.add(text);ht.br();ht.br()

            if ht.canBeProcessed:
                ht.add("Value can be interpreted.")
            else:
                ht.add("Value can not be interpreted.")

            if ht.processed:
                ht.add("Value has been interpreted. ")
                q = ht.queryComponents.copy()
                q["raw"] = 1
                with ht.a(href=ht.baseUrl + "/?" + urllib.urlencode(q, doseq=1)):
                    ht.add("View raw data.")
            else:
                ht.add("Value has not been interpreted.")
                if ht.canBeProcessed:
                    q = ht.queryComponents.copy()
                    q["raw"] = 0
                    with ht.a(href=ht.baseUrl + "/?" + urllib.urlencode(q, doseq=1)):
                        ht.add("View processed data.")

        if fetchError:  # to be more clear
            ht.add(fetchError)

    return ht  # explicit return

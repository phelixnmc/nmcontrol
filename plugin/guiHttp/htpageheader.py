def writeMenuEntry(ht, text):
    with ht.div(class_="menuItem"):
        if ht.currentPage == text:
            with ht.div(class_="menuItemActive"):
                ht.add(text)
        else:
            with ht.a(href=ht.baseUrl + "/?p=" + text):
                ht.add(text)

def render(ht):
    title = "NMControl HTTP GUI"
    styles = (ht.baseUrl + '/static/style_v01.css')

    ht.init(title=title, css=styles)

    with ht.div():
        with ht.div(style="border=0;" +
                            "background-color:#61B0DE;" +
                            "background: -moz-linear-gradient(top, #93C2DE, #2E4E61);" +
                            "background: -webkit-gradient(linear, left top, left bottom, from(#93C2DE), to(#2E4E61));" +
                            "padding:20px;"):
            ht.img(src=ht.baseUrl + "/static/nmctrl.svg", alt="nmctrl", width="260")
            with ht.div(style="width:1000px;padding:0px;margin:0px;padding-left:40px;"):
                with ht.h1():
                    ht.add("Namecoin Control Center")
                for m in ht.menuEntries:
                    writeMenuEntry(ht, m)
    return ht  # explicit return

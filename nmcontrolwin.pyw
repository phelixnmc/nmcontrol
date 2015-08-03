#!/usr/bin/env python

# On windows the file extension .pyw hides the console window

try:
    # display splashscreen
    import sys
    sys.path.append("lib")
    import splashscreen
    splashscreen.splash('lib/splash.gif')

    import nmcontrol
    nmcontrol.main()
except:
    # GUI Error Output

    import traceback

    # Be prepared for Python3
    try:
        import Tkinter as tkinter
    except ImportError:
        import tkinter

    root = tkinter.Tk()
    tkinter.Label(root, justify="left", text=traceback.format_exc()).pack()
    tkinter.Button(root, text="OK", command=root.quit).pack()
    root.mainloop()

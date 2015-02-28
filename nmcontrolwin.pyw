#!/usr/bin/env python

"""
On windows the file extension .pyw hides the console window
"""

class Unbuffered(object):
    """workaround for unbuffered stdout to file on py2 and py3 from so"""
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

try:
    import os
    import sys
    sys.path.append("lib")

    # redirect console output to file as there is no console
    import platformDep
    outputFilename = platformDep.getNmcontrolDir() + os.sep + "output.log"
    f = open(outputFilename, 'w')  # will overwrite the file on every start
    sys.stdout = Unbuffered(f)  # neither unbuffered nor line buffered seems to work properly on both py2 and py3
    #sys.stderr = f

    import splashscreen
    splashscreen.splash('lib/splash.gif')

    import nmcontrol
    nmcontrol.main()
except:
    # GUI error output on crash

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
try:
    f.close()
except:
    pass

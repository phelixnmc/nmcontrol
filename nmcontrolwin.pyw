#!/usr/bin/env python

"""
On windows the file extension .pyw hides the console window
"""

outputFilename = "output.log"

import time
import os
import sys
sys.path.append("lib")

class Unbuffered(object):
    """workaround for unbuffered stdout to file on py2 and py3 from so"""
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        for line in data.rstrip().splitlines():
            self.stream.write(time.strftime("%Y-%m-%d %H:%M:%S") + " "  + line + "\n")
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

try:
    import platformDep
    import splashscreen
    import nmcontrol

    # redirect console output to file as there is no console
    outputPath = platformDep.getNmcontrolDir()
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    f = open(outputPath + os.sep + outputFilename, 'w')  # will overwrite the file on every start
    sys.stdout = Unbuffered(f)  # neither unbuffered nor line buffered seems to work properly on both py2 and py3
    sys.stderr = Unbuffered(f)

    splashscreen.splash('lib/splash.gif')

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
    tkinter.Label(root, justify="left", text=traceback.format_exc() +
    "\n\nThere might be more information in %APPDATA%\output.log").pack()
    tkinter.Button(root, text="OK", command=root.quit).pack()
    root.mainloop()

time.sleep(0.2)  # wait until all processes have shut down and stopped writing to stdout
try:
    f.close()
except:
    pass

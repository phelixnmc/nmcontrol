
app = {}


# logging

LOGFILENAME = "log.txt"

import sys
sys.path.append("lib")
import mylogging

def get_logger(name):
    global app

    level = mylogging.INFO
    if app['debug']:
        level = mylogging.DEBUG

    logFilenamePath = app["path"]["conf"] + "/" + LOGFILENAME
    return mylogging.get_my_logger(name, levelConsole=level, filename=logFilenamePath, levelFile=level)

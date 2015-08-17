
app = {}


# logging

logFilenamePath = None

imports sys
sys.path.append("lib")
import mylogging

def get_logger(name):
    global app

    level = mylogging.INFO
    if app["debug"]:
        level = mylogging.DEBUG

    logFilenamePath = app["path"]["conf"] + "/" + "log.txt"
    return mylogging.get_my_logger(name, levelConsole=level, filename=logFilenamePath, levelFile=level)

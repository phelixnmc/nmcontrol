
app = {}


# logging
import mylogging
import platformDep

LOGTOFILE = True  # will be set to False for client mode
LOGFILENAME = "log.txt"

def get_logger(name, clear=False):
    global app

    level = mylogging.INFO
    if app['debug']:
        level = mylogging.DEBUG

    logFilenamePath = None
    if LOGTOFILE:
        logFilenamePath = platformDep.getNmcontrolDir() + "/" + LOGFILENAME

    return mylogging.get_my_logger(name, levelConsole=level, filename=logFilenamePath,
                                   levelFile=level, clear=clear)


app = {}


# logging
import mylogging
import platformDep

LOGFILENAME = "log.txt"

def get_logger(name, clear=False):
    global app

    level = mylogging.INFO
    if app['debug']:
        level = mylogging.DEBUG

    logFilenamePath = platformDep.getNmcontrolDir() + "/" + LOGFILENAME
    return mylogging.get_my_logger(name, levelConsole=level, filename=logFilenamePath,
                                   levelFile=level, clear=clear)

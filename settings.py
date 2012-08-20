import logging
import logging.handlers
import os
from platform import node

#Import all of the defaults settings
from settings_defaults import *

if node() == DEVELOPMENT_HOST:
    from settings_development import *
elif node() == TEST_HOST:
    from settings_test import *
elif node() == PRODUCTION_HOST:
    from settings_production import *
else:
    #If a local settings file is found then use it.
    #This file is ignored within svn -- reference settings_local_sample to create your own
    try:
        from settings_local import *
    except ImportError:
        raise Exception("Cannot determine execution mode for host '%s'. Please check DEVELOPMENT_HOST, TEST_HOST and PRODUCTION_HOST in settings_defaults.py." % node())

#Finally set up logging

#Logging settings
LOG_DIR = os.path.join(PROJECT_ENV_PATH, "logs")
LOG_FILE = os.path.join(LOG_DIR, "picbadge.log")

if not hasattr(logging, "set_up_done"):
    logging.set_up_done=False

def set_up():
    if logging.set_up_done:
        return
    log = logging.getLogger("picbadge")
    log.level = LOG_LEVEL
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # log to console 
    #ch = logging.StreamHandler() 
    #ch.setFormatter(formatter) 
    #log.addHandler(ch)
    
    # log to file 
    fh = logging.handlers.RotatingFileHandler(LOG_FILE, 'a', 1000000, 10) 
    fh.setFormatter(formatter) 
    log.addHandler(fh) 
    
    logging.set_up_done=True
    
set_up()
import logging
import os

#Logging settings
LOG_DIR = os.path.join(PROJECT_ENV_PATH, "logs")
LOG_FILE = os.path.join(LOG_DIR, "picbadge.log")

log = logging.getLogger("picbadge")
log.level = LOG_LEVEL
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# log to console 
#ch = logging.StreamHandler() 
#ch.setFormatter(formatter) 
#log.addHandler(ch)

# log to file 
fh = logging.FileHandler(LOG_FILE) 
fh.setFormatter(formatter) 
log.addHandler(fh) 
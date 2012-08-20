import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PICBADGEAPI_URL = "http://devsnowdev.org/api/picbadge/"
PICBADGEAPI_PATH = ""
STATIC_ROOT = 'The/absolute/path/to/the/directory/where/collectstatic/will/collect/static/files/for/deployment'
METRICS_INSTANCE="yourcompanyLocal"
METRICS_URL="http://your-integration-servername:9180/metrics/"
PROJECTS_PATH = "/your/project/path"
PROJECT_ENV_PATH = os.path.join(PROJECTS_PATH, "dev")
LOG_LEVEL=logging.DEBUG

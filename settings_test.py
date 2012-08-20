import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PICBADGEAPI_URL = "http://testservername.org/api/picbadge"
PICBADGEAPI_PATH = ""
STATIC_ROOT = 'testing/absolute/path/to/the/directory/where/collectstatic/will/collect/static/files/for/deployment'
METRICS_URL="http://your-qa-servername:9180/metrics/"
METRICS_INSTANCE="metricsTest"
PROJECTS_PATH = "/your/project/path"
PROJECT_ENV_PATH = os.path.join(PROJECTS_PATH, "test")
LOG_LEVEL=logging.DEBUG

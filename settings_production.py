import logging
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PICBADGEAPI_URL = "http://yourcompany.org/api/picbadge"
PICBADGEAPI_PATH = ""
STATIC_ROOT = 'Production/absolute/path/to/the/directory/where/collectstatic/will/collect/static/files/for/deployment'
METRICS_URL="http://your-production-servername:9180/metrics/"
METRICS_INSTANCE="yourcompanyProd"
PROJECTS_PATH = "/your/project/path"
PROJECT_ENV_PATH = os.path.join(PROJECTS_PATH, "prod")
LOG_LEVEL=logging.DEBUG

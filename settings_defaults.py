# Django settings for polarCommonProj project.
import sys

from os.path import join, dirname, normpath

# Used to provide absolute paths. Normally the default is fine.
LOCAL_PATH = normpath(join(dirname(__file__), '..'))

DATACASTER = "datacaster"
PICBADGEURL = "picbadge"
PICBADGEAPIURL = "picbadgeapi"
PICBADGEAPI_PATH = "picbadgeapi"
PICBADGEPATH = normpath(join(dirname(__file__), 'picBadge'))
PROJECTS_PATH = "/your/projects/path"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
# These database settings don't do any harm as long as we aren't using a database
# Values are only set to avoid issues with the test engine
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = './testdb'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = normpath(join(dirname(__file__), 'picBadge'))

DC_TEMP_DIR = '/tmp/cast/'

# STATIC_ROOT = 'The/absolute/path/to/the/directory/where/collectstatic/will/collect/static/files/for/deployment'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/picbadge/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'thisissomesecretkeywithabunchofsymbolsinit'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'polarCommonProj.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    normpath(join(dirname(__file__), 'picBadge/templates')),
    normpath(join(dirname(__file__), 'datacaster/templates')),    
)

INSTALLED_APPS = (
    #'django.contrib.admin',
	#'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'polarCommonProj.picBadge',
    'polarCommonProj.picBadgeAPI',
    'polarCommonProj.datacaster',
)

# These are the hostnames as returned by platform.node().
# If you aren't sure what to put, leave them blank and the error message should tell you which hostname Python sees.
DEVELOPMENT_HOST = 'your-integration-servername'
TEST_HOST = 'your-qa-servername'
PRODUCTION_HOST = 'your-production-servername'

import os, sys

sys.path.append('/WEB/APPS/python')
sys.path.append('/WEB/APPS/python/polarCommonProj')

os.environ['DJANGO_SETTINGS_MODULE'] = 'polarCommonProj.settings'

import django.core.handlers.wsgi

#_application = django.core.handlers.wsgi.WSGIHandler()
#def application(environ, start_response):
#    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
#    environ['SCRIPT_NAME'] = '' # my little addition to make it work
#    return _application(environ, start_response)

application = django.core.handlers.wsgi.WSGIHandler()

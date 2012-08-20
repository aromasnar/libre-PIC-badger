from django.conf.urls.defaults import *
from django.conf import settings
from polarCommonProj.picBadge.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    
	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
	
	# PIC Badge application URLs
	# main page
	(r'^$'	, onePagePICBadge),	
	
	# proxy for ajax calls from onepage picbadge app
	(r'^createBadge/$', createBadge),	 	
    (r'^createBadge$', createBadge),
	
)

if settings.DEBUG:
    urlpatterns += patterns('',
	(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
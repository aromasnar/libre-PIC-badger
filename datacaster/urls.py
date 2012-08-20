from django.conf.urls.defaults import *
from django.conf import settings
from polarCommonProj.datacaster.views import *

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
	(r'^$'	, index),	
	(r'^static/(?P<path>.*)$', 'django.views.static.serve' ,{'document_root' : settings.STATIC_ROOT}),
        
    (r'^tmp/(?P<cast_name>[a-zA-Z0-9-_]{1,50}).xml$', 'polarCommonProj.datacaster.views.fetch_cast'),
      
     (r'^save-cast$', 'polarCommonProj.datacaster.views.save_cast'),
    
    (r'^load-cast$', 'polarCommonProj.datacaster.views.load_cast'),

    (r'^load-cast-url$', 'polarCommonProj.datacaster.views.load_cast_from_url'),

    (r'^pub-cast-email$', 'polarCommonProj.datacaster.views.pub_cast_email'),
    
    (r'^save-cast-no-save/(?P<cast_name>[a-zA-Z0-9-_]{1,50}).xml$', 'polarCommonProj.datacaster.views.bounce_cast'),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
	(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	)
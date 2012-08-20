from django.conf.urls.defaults import *
from django.conf import settings
import settings
import os

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

	# FOR PIC BADGE... refering to the badging application's url configuration
	(r'^%s/' % settings.PICBADGEURL, include('polarCommonProj.picBadge.urls')),
	
	# FOR PIC BADGE API... refering to the api url configuration
	(r'^%s/' % settings.PICBADGEAPIURL, include('polarCommonProj.picBadgeAPI.urls')),	
    
    (r'^%s/' % settings.DATACASTER, include('polarCommonProj.datacaster.urls')),
)

# PIC Badge API's urls.py

from django.conf.urls.defaults import *
#from piston.resource import Resource
from polarCommonProj.picBadgeAPI.resource import Resource
from piston.authentication import HttpBasicAuthentication
from polarCommonProj.picBadgeAPI.handlers import *

from polarCommonProj.picBadgeAPI.handlers import getLicenseClassesHandler
from polarCommonProj.picBadgeAPI.metricsRecorder import *

auth = HttpBasicAuthentication(realm="My Realm")
ad = { }

getLicenseClasses_resource = Resource(handler=getLicenseClassesHandler, **ad)
issueCCZero_resource= Resource(handler=issueCCZeroHandler, **ad)
issueCCBy_resource= Resource(handler=issueCCByHandler, **ad)
getCCZeroFields_resource= Resource(handler=getCCZeroFieldsHandler, **ad)
getCCByFields_resource= Resource(handler=getCCByFieldsHandler, **ad)
getCCZeroTerritories_resource = Resource(handler=getCCZeroTerritoriesHandler, **ad)
getCCZeroAgreement_resource = Resource(handler=getCCZeroAgreementHandler, **ad)
getCCByAgreement_resource = Resource(handler=getCCByAgreementHandler, **ad)
testJson_resource = Resource(handler=testJsonHandler, **ad)

urlpatterns = patterns('',
    url(r'^licenses/$', getLicenseClasses_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_zero/issue/$', issueCCZero_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_by/issue/$', issueCCBy_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_zero/territories/$', getCCZeroTerritories_resource, { 'emitter_format': 'xml'}),
    url(r'^licenses/pic_cc_zero/agreement/$', getCCZeroAgreement_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_by/agreement/$', getCCByAgreement_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_zero/$', getCCZeroFields_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/pic_cc_by/$', getCCByFields_resource, { 'emitter_format': 'xml' }),
    url(r'^licenses/testjson/$', testJson_resource, { 'emitter_format': 'xml' }),
)

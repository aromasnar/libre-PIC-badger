# Author:	Azhar Sikander
# This file contains all the views for the badging application.
			
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render_to_response
from polarCommonProj.picBadge.models import cc0UserInfoForm
from polarCommonProj.picBadge.models import ccByUserInfoForm
#from polarCommonProj.picBadge.ccLicenseAPI.rest import CcRest
from polarCommonProj.picBadge.picBadgeAPIClient.picBadgeAPIClient import picAPIClient
from polarCommonProj.picBadge.scripts.ErrorHandling import ErrorHandler
from polarCommonProj.picBadgeAPI.metricsRecorder import metricRecorder

from django.utils import simplejson
from django.conf import settings
import urllib
import urllib2
import re
from datetime import datetime
from polarCommonProj.picBadge.LocalTimezone import LocalTimezone
import logging
from django.utils.http import urlquote  as django_urlquote



log = logging.getLogger("picbadge.views")


def getLicenseFromCCWebsite():
	return True

# This view creates the main page of the badging app. 
def onePagePICBadge(request):		
	# creating zero waiver and CC By license form objects. forms are defined in Models.py
	zeroform = cc0UserInfoForm()
	ccByform = ccByUserInfoForm()

	# Dynamically create the badging app's main page using the two form objects.
	return render_to_response('sub_template.html', {'form1':zeroform, 'form2':ccByform})	

# Handles Ajax call from the Badging App. And generates badges using pic api.
def createBadge(request):	
	errHandler = ErrorHandler()
	# what license to generate?	
	licenseType = request.POST['licenseType']
	formID = request.POST['formID']
	

	# PIC RESTful webservice URL = http://testservername.org/picbadgeapi...
	# creating pic client api object.
	picserver = picAPIClient(settings.PICBADGEAPI_URL + settings.PICBADGEAPI_PATH) 
	
	# We've got a pic_CCBy license application.
	if licenseType == "pic_cc_by":
		form = ccByUserInfoForm(request.POST)
		
	# We've got a pic_zero license application.
	elif licenseType == 'pic_cc_zero':
		form = cc0UserInfoForm(request.POST)
		
	# Invalid call
	else:
		response = {"status": "error", "response": errHandler.InvalidInputError()}
	
	# checks if the form data is valid w.r.t. CC by form specification.
	if form.is_valid():			
		try:				
			cd = form.cleaned_data							
			userInfo = cd.copy()			
			# removing the form element that are not required for licensing.
			del userInfo['agreementconfirm']
		except:
			errMsg = errHandler.PythonError()
			response = {"status": "error", "response": errMsg}
		
		try:
			# this module of the client api forms the answers xml and calls PIC Licensing webservice
			licenseOutput = picserver.getLicense(licenseType, userInfo)
			response = {"status": "license", "response": licenseOutput}
			
			
		except:
			errMsg = errHandler.PICAPIError()
			response = {"status": "error", "response": errMsg}
		
	else:				
		t = get_template('form_template.html')
		formHtml = t.render(Context({'formID' : formID, 'dataForm' : form}))
		response = {"status": "validationError", "response": formHtml}
	
	#Notify the metrics services
	
	log.debug("Notifying metrics service.")	
	try:
		metricRec= metricRecorder()
		metricRec.newInstance(request,'PICBadgeGUI','Libre')

		# We've got a pic_CCBy license application.
		if licenseType == "pic_cc_by":
			metrics_url = request.POST['workurl']
					
		# We've got a pic_zero license application.
		elif licenseType == 'pic_cc_zero':
			metrics_url = request.POST['attribution_url']
			metricRec.addMetric("Territory",request.POST['territory'])
					
		metrics_title = request.POST['title']		
		metrics_api_HttpCodeResponse= picserver.getHttpResponse()
		if metrics_api_HttpCodeResponse==200:
			metrics_success="True"
		else:
			metrics_success="False"
		
		
		metricRec.addMetric("LicenseType",licenseType)			
		metricRec.addMetric("Url",metrics_url)
		metricRec.addMetric("Title",metrics_title)		
		metricRec.addMetric("Success",metrics_success)		
		metricRec.sendMetric()
		
		

		
	except IOError as e:
		log.error("Error occurred sending metrics to service.")
		log.error (e)
		
	jsonOutput = simplejson.dumps(response)
	log.debug( jsonOutput )
	
	return HttpResponse(jsonOutput, mimetype='application/json')
	

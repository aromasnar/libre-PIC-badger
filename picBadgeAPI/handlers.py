# Author:   Azhar Sikander
# Contains all the web services provided by the PIC Badge API

from piston.handler import BaseHandler
from piston.emitters import XMLEmitter
from piston import *
from piston.utils import *
from django.http import Http404, HttpResponse, HttpResponseNotAllowed
from django import forms
from polarCommonProj.picBadgeAPI.scripts.licenses import picLicenses
from polarCommonProj.picBadge.models import cc0UserInfoForm
from polarCommonProj.picBadge.models import ccByUserInfoForm
from polarCommonProj.picBadgeAPI.scripts.CCLicenseProcessor import *
from polarCommonProj.picBadgeAPI.scripts.ErrorHandling import *
from polarCommonProj.picBadgeAPI.resource import validate
from polarCommonProj.picBadgeAPI.metricsRecorder import metricRecorder
#from django.views.decorators.csrf import csrf_exempt

import urllib2
import lxml.etree
from lxml import objectify
from StringIO import StringIO
import sys
import logging
import re

errHandler = ErrorHandler()

log = logging.getLogger("picbadge.handlers")

class getLicenseClassesHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self, request):
		
		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetLicenses')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
			
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getLicenseClasses())
		
class getCCZeroFieldsHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self,request):

		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetFields')
			metricRec.addMetric('LicenseType','pic_cc_zero')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
			
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getLicenseAttributes('pic_cc_zero'))

class getCCByFieldsHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self,request):
		
		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetFields')
			metricRec.addMetric('LicenseType','pic_cc_by')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
			
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getLicenseAttributes('pic_cc_by'))
		
class issueCCZeroHandler(BaseHandler):	
	allowed_methods = ('GET', 'POST',)
	
	@classmethod
	def create(self, request):
		# Creative Commons licensing web Service URL
		cc_url = 'http://api.creativecommons.org/rest/staging/license/zero/issue'	
	
		metricRec= metricRecorder()
		metricRec.newInstance(request,'PICBadgeAPI','Libre')
		metricRec.addMetric('ServiceEndpoint','IssueLicense')
		metricRec.addMetric("LicenseType",'pic_cc_zero')
		
		log.debug("Creating CC Zero Badge...")
		try:
			# get user information from the request.
			if request.content_type:
				log.debug("Received %s data..." % (request.content_type))
				answers = request.raw_post_data
			else:
				log.debug("Received form data...")
				answers = request.POST.get('answers','')
			#remove <?xml...?> header, as it seems to have problems with encoding
			answers = re.sub('<\?.*?\?>','',answers)
			log.debug("Answers is: %s" % answers)
			doc = lxml.etree.parse(StringIO(answers))
			
			#extact output type from answers
			outputType = doc.xpath('//answers/outputType')	
			outputType = outputType[0].text		
			metricRec.addMetric('OutputType',outputType)
			metrics_title=doc.xpath('//answers/work-info/title')[0].text
			metrics_url=doc.xpath('//answers/work-info/attribution_url')[0].text
			metrics_territory=doc.xpath('//answers/work-info/territory')[0].text
			
			metricRec.addMetric("Territory",metrics_territory)
			metricRec.addMetric("Url",metrics_url)
			metricRec.addMetric("Title",metrics_title)
			
			metrics_source=doc.xpath('//answers/source')
			if (not metrics_source):
				metrics_source='api'
			else:
				metrics_source=metrics_source[0].text
			metricRec.addMetric("Source", metrics_source)
			
			metricRec.sendMetric()
			
			
			root = doc.getroot()
			root.remove(root.find("outputType"))
			
			# Create anwers xml to request license from CC WebService.
			newAnswers = lxml.etree.Element("answers")
			newAnswersDoc = lxml.etree.ElementTree(newAnswers)
			localeNode = lxml.etree.SubElement(newAnswers, "locale")
			localeNode.text = "en"
			localeNode = lxml.etree.SubElement(newAnswers, "license-zero")
			# appending user information into the answers
			newAnswers.append(root.find("work-info"))	
			
			
			
			
			newAnswers = lxml.etree.tostring(newAnswersDoc)	
			
		except Exception as ex:
			log.debug("Exception while reading answers...")
			log.debug(ex)
			return HttpResponse(errHandler.PythonError())			
		
		# get license from CC Webservice
		try:
			CCLicenseXML = urllib2.urlopen(cc_url, data='answers=%s' % newAnswers).read()					
		except:
			return HttpResponse(errHandler.CCServerError())
		
		# embed PIC logo into the license
		try:
			licenseXMLProcessor = CCLicenseProcessor()	
			licenseXMLProcessor.setLicenseType("zero")		
			CCLicenseXMLwithPIC = licenseXMLProcessor.embeddPICLOGO(CCLicenseXML)
		except:
			return HttpResponse(CCLicenseXML)#"Error occured while generating license. please verify you sent valid data.")
		
		if outputType == "html":
			try:
				htmlOnly = licenseXMLProcessor.extractLicenseHTML(CCLicenseXMLwithPIC)
			except:
				return HttpResponse(CCLicenseXMLwithPIC)
				
			return HttpResponse(htmlOnly)			
		else:
			return HttpResponse(CCLicenseXMLwithPIC)		
			
class issueCCByHandler(BaseHandler):	
	allowed_methods = ('GET', 'POST',)
	
	@classmethod
	def create(self, request):
		# Creative Commons licensing web Service URL
		cc_url = 'http://api.creativecommons.org/rest/staging/license/standard/issue'
		log.debug("Creating CC By Badge...")
		
		metricRec= metricRecorder()
		metricRec.newInstance(request,'PICBadgeAPI','Libre')
		metricRec.addMetric('ServiceEndpoint','IssueLicense')
		metricRec.addMetric("LicenseType",'pic_cc_by')
		
		
		try:		
			# get user information from the request.
			if request.content_type:
				log.debug("Received %s data..." % (request.content_type))
				answers = request.data
			else:
				log.debug("Received form data...")
				answers = request.POST.get('answers','')
			#remove <?xml...?> header, as it seems to have problems with encoding
			answers = re.sub('<\?.*?\?>','',answers)
			
			answers = request.POST.get('answers','')
			doc = lxml.etree.parse(StringIO(answers))
			
			#extact output type from answers
			outputType = doc.xpath('//answers/outputType')	
			outputType = outputType[0].text
			
			metricRec.addMetric('OutputType',outputType)
			metrics_title=doc.xpath('//answers/work-info/title')[0].text
			metrics_url=doc.xpath('//answers/work-info/work-url')[0].text
			metricRec.addMetric("Url",metrics_url)
			metricRec.addMetric("Title",metrics_title)						
			
			metrics_source=doc.xpath('//answers/source')
			if (not metrics_source):
				metrics_source='api'
			else:
				metrics_source=metrics_source[0].text
			metricRec.addMetric("Source", metrics_source)			
			
			metricRec.sendMetric()						
			
			root = doc.getroot()
			root.remove(root.find("outputType"))
			
			# Create anwers xml to request license from CC WebService.
			newAnswers = lxml.etree.Element("answers")
			newAnswersDoc = lxml.etree.ElementTree(newAnswers)
			localeNode = lxml.etree.SubElement(newAnswers, "locale")
			localeNode.text = "en"
			localeNode = lxml.etree.SubElement(newAnswers, "license-standard")
			
			# these answers are fixed... as per PIC CC BY license specification
			dnode = lxml.etree.SubElement(localeNode, "commercial")
			dnode.text = 'y'
			dnode = lxml.etree.SubElement(localeNode, "derivatives")
			dnode.text = 'y'
			dnode = lxml.etree.SubElement(localeNode, "jurisdiction")
			dnode.text = 'Generic'
			# appending user information into the answers
			newAnswers.append(root.find("work-info"))	
			
			newAnswers = lxml.etree.tostring(newAnswersDoc)
		
		except Exception as ex:
			log.debug("Exception while reading answers...")
			log.debug(ex)
			return HttpResponse(errHandler.PythonError())						
		
		# get license from CC Webservice
		try:
			CCLicenseXML = urllib2.urlopen(cc_url, data='answers=%s' % newAnswers).read()					
		except:
			return HttpResponse(errHandler.CCServerError())
		
		# embed PIC logo into the license
		try:
			licenseXMLProcessor = CCLicenseProcessor()
			licenseXMLProcessor.setLicenseType("by")
			CCLicenseXMLwithPIC = licenseXMLProcessor.embeddPICLOGO(CCLicenseXML)
		except:
			return HttpResponse(CCLicenseXML)#"Error occured while generating license. please verify you sent valid data.")
		
		if outputType == "html":
			try:
				htmlOnly = licenseXMLProcessor.extractLicenseHTML(CCLicenseXMLwithPIC)
			except:
				return HttpResponse(CCLicenseXMLwithPIC)
				
			return HttpResponse(htmlOnly)			
		else:
			return HttpResponse(CCLicenseXMLwithPIC)
			
			
class getCCZeroTerritoriesHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self,request):
		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetTerritories')
			metricRec.addMetric('LicenseType','pic_cc_zero')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
			
		log.debug("Request for CC0 Territories list...")
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getTerritories())
	

class getCCZeroAgreementHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self,request):
		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetAgreement')
			metricRec.addMetric('LicenseType','pic_cc_zero')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
					
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getLicenseAgreement('pic_cc_zero'))
	

class getCCByAgreementHandler(BaseHandler):
	allowed_methods = ('GET',)
	
	@classmethod
	def read(self,request):
		try:		
			metricRec= metricRecorder()
			metricRec.newInstance(request,'PICBadgeAPI','Libre')
			metricRec.addMetric('ServiceEndpoint','GetAgreement')
			metricRec.addMetric('LicenseType','pic_cc_by')
			metricRec.sendMetric()
		except IOError as e:
			log.debug("Error while calling the metric client")
			log.error (e)
			
		pic_cc_licenses = picLicenses()
		return HttpResponse(pic_cc_licenses.getLicenseAgreement('pic_cc_by'))
	
	
class TestJsonForm(forms.Form):
	test = forms.CharField(required=True)
	
class testJsonHandler(BaseHandler):
	allowed_methods = ('POST',)
	
	@validate(TestJsonForm)
	def create(self, request):
		log.debug("Creating CC Zero Badge...")
		if request.content_type:
			log.debug("Received %s data..." % (request.content_type))
			answers = request.data
		else:
			log.debug("Received form data...")
			answers = request.POST.get('test','')
		log.debug("Answers is: %s" % answers)
		
		doc = Document()
		
		#create root node "territories"
		output = doc.createElement("output")
		outputText = doc.createTextNode(answers)
		output.appendChild(outputText)
		doc.appendChild(output)
		
		return HTTPResponse(doc)

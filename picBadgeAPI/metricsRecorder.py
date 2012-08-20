# Author:   Luis Lopez
# Metric recording class


from django.conf import settings
from piston.utils import *
from datetime import datetime
from polarCommonProj.picBadge.LocalTimezone import LocalTimezone
import logging
import urllib2
import urllib

class metricRecorder():
	'''
	MetricRecorder class to simplify the metrics recording
	'''
	log=None	
	clientIP = "None"
	XML_model_head=None
	XML_model_tail=None
	XML_model_metrics=None
	
	
	def newInstance(self,Request,serviceName,sponsor):
		'''
		Creates a Sample with the data from the current Requested session
		'''
		self.log = logging.getLogger("picbadgeAPI.metrics")	
		self.log.debug("Creating a metric recorder")
		
		
		try:
			self.cientIP = Request.META['HTTP_X_FORWARDED_FOR']
		except KeyError:
			self.clientIP = Request.META['REMOTE_ADDR']

			
		self.time=datetime.now(LocalTimezone()).strftime("%Y-%m-%dT%H:%M:%S.%f%z")
		self.userAgent=Request.META["HTTP_USER_AGENT"]
		self.session=""
		self.instance=settings.METRICS_INSTANCE
		self.serviceName = serviceName
		self.sponsor = sponsor
	
		self.XML_model_head="""
		<sample>
				<entryTs>%s</entryTs>
				<ipAddress>%s</ipAddress>
				<sessionId>%s</sessionId>
				<userAgent>%s</userAgent>
		""" % (self.time,self.clientIP,self.session,'<![CDATA['+ self.userAgent +']]>')
		self.XML_model_head='<?xml version="1.0" encoding="UTF-8"?> \n' + self.XML_model_head
		
		self.XML_model_tail="""<service>
				<instance>%s</instance>
				<serviceName>%s</serviceName>
				<sponsor>%s</sponsor>
				</service>
				</sample>""" %(self.instance, serviceName, sponsor)
		
		self.XML_model_metrics=""
		
	
	
	
	
	def addMetric(self,name,value):
		'''
		Adds pairs of values to the current sample
		'''
		name=str(name)
		value=str(value)
		metric="""
		<metrics>
			<name>%s</name>
			<value>%s</value>
		</metrics>		
		""" % (name,value)
		
		self.XML_model_metrics += metric
		
	
	def sendMetric(self):
		self.log = logging.getLogger("picbadgeAPI.metrics")	
		self.log.debug("Notifying metrics service.")	
		try:

			# Having trouble getting a session id consistently -- need to investigate
			# m = re.search(r"JSESSIONID=(\w+);",request.META["HTTP_COOKIE"])
			#if m is not None:
		    #		sessionId = m.group(1)
			# Set up the request to the metrics api
			
			metric_xml=self.XML_model_head + self.XML_model_metrics + self.XML_model_tail		
			metric_xml = metric_xml.replace('\n', '')
			metric_xml = metric_xml.replace('\t', '')  
			
			headers = { 'Content-Type': 'application/xml' }
			
			metricsUrl = settings.METRICS_URL + "projects/%s/services/%s/instances/%s" % (self.sponsor, self.serviceName, settings.METRICS_INSTANCE)
			
			self.log.debug(metric_xml)
			self.log.debug(headers)
			self.log.debug(metricsUrl)		
			metricsPostReq = urllib2.Request(metricsUrl, metric_xml, headers)        

			metricResponse = urllib2.urlopen(metricsPostReq)
			metricResponse = metricResponse.read()
		
			self.log.debug("Metric logged to service.")
			#self.log.debug(metricResponse)
			
		except IOError as e:
			self.log = logging.getLogger("picbadgeAPI.metrics")	
			self.log.error("Error occurred sending metrics to service.")
			self.log.error (e)
			

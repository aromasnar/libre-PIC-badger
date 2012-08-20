# Author:	Azhar Sikander
# This file contains PIC API Client that process user information dictionary and creates 
# an answers xml. and then calls pic licensing web service to get the speicified license.


import urllib
import urllib2
import lxml.etree
from StringIO import StringIO
import sys
import os
import logging

log = logging.getLogger("picbadge.picBadgeAPIClient")

class picAPIClient:
    """Wrapper class to decompose REST XML responses into Python objects."""
    
    httpResponseCode=0     
    
    def getLicense(self, license, userInfo):
        l_url = '%s/licenses/%s/issue/' % (self.root, license)
        # construct the answers.xml document from the answers dictionary
        answer_xml = """<answers>"""
        
        answer_xml = """%s<work-info>""" %(answer_xml)
        
        for key in userInfo:
            indexKey = key
            if (key == 'sourceurl'):
                    key = 'source-url'
            if (key == 'workurl'):
                    key = 'work-url'
					
			# outputType is not under work-info.
            if (key != 'outputType'):
                answer_xml = """%s<%s>%s</%s>""" % (answer_xml, key, userInfo[indexKey], key)
        
        answer_xml = """%s</work-info>"""% (answer_xml)
            
        answer_xml = """%s<outputType>%s</outputType><source>gui</source></answers>""" % (answer_xml, userInfo['outputType'])
		
        log.debug(answer_xml)
        
		# retrieve the license source document
        try:
            # Set up the request to the badger api using form data as xml string
            req = urllib2.Request(l_url, "answers=%s" % answer_xml)
            # Call the badger api 
            response = urllib2.urlopen(req)
            self.httpResponseCode = response.code
            license_doc = response.read()     
        except:
            license_doc = "Unable to connect to PIC API Webservice"	
            self.httpResponseCode=500
			
        return license_doc
    def getHttpResponse(self):
        return self.httpResponseCode
	
    def __init__(self, root):
        self.root = root
		
# client API test code.
# ---------------------

# picserver = picAPIClient('http://testservername.org/picbadgeapi')
# userInfo = {'title':'azsdf', 'attribution_url':'ddd','territory':'US','creator':'dddd','outputType':'html'}
# output = picserver.getLicense('pic_cc_zero', userInfo)
# print output

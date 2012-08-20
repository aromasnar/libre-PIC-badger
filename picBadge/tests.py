"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from polarCommonProj.picBadge.picBadgeAPIClient.picBadgeAPIClient import picAPIClient
from polarCommonProj.picBadge.configurationReader import configReader
from polarCommonProj.picBadge.models import cc0UserInfoForm
from polarCommonProj.picBadge.models import ccByUserInfoForm
from django.conf import settings 
from django.conf import settings

import urllib2
import lxml.etree
from lxml import objectify
from StringIO import StringIO

class picBadgeAppTestCases(TestCase):
    picAPIURL = settings.PICBADGEAPI_URL + "/" + settings.PICBADGEAPI_PATH
    
    def test_picBadgeURL(self):
        success = '1'
        req = urllib2.Request('http://yourcompany.org/libre/apps/picbadge/')
        # Call the badger api 
        try:
            response = urllib2.urlopen(req)
        except:
            # means URL is not valid.
            success = '0'                
        self.failUnlessEqual(success, "1")
        
    def test_picZeroForm(self):
        success = '1'
        try:
            form = cc0UserInfoForm()
        except:
            success = '0'
        self.failUnlessEqual(success, "1")
        
    
    def test_picCCByForm(self):
        success = '1'
        try:
            form = ccByUserInfoForm()
        except:
            success = '0'
        self.failUnlessEqual(success, "1")
    
    def test_picAPIConnectionForPicZeroHTML(self):
        picserver = picAPIClient(self.picAPIURL)
        
        """testing for HTML output"""
        userInfo = {'title':'test_title', 'attribution_url':'test_attr_url','territory':'US','creator':'test_creator','outputType':'html'}
        output1 = picserver.getLicense('pic_cc_zero', userInfo)        
        tree = lxml.etree.parse(StringIO(output1))
        root = tree.getroot()
        self.failUnlessEqual(root.tag, "html")        
        
    def test_picAPIConnectionForPicZeroXML(self):
        picserver = picAPIClient(self.picAPIURL)
        
        """testing for XML output"""
        userInfo = {'title':'test_title', 'attribution_url':'test_attr_url','territory':'US','creator':'test_creator','outputType':'xml'}
        output2 = picserver.getLicense('pic_cc_zero', userInfo)
        tree = lxml.etree.parse(StringIO(output2))
        root = tree.getroot()
        self.failUnlessEqual(root.tag, "result")
        
        
    def test_picAPIConnectionForPicCCByHTML(self):
        picserver = picAPIClient(self.picAPIURL)
        """testing for HTML output""" 
        
        userInfo = {'title':'test_title', 'workurl':'test_work_url', 'type':'test_type', 'year':'test_year', 'description':'test_desc', 'creator':'test_creator', 'holder':'test_holder', 'outputType':'html'}
        output = picserver.getLicense('pic_cc_by', userInfo)
        tree = lxml.etree.parse(StringIO(output))
        root = tree.getroot()
        self.failUnlessEqual(root.tag, "html")     
        
    
    def test_picAPIConnectionForPicCCByXML(self):
        picserver = picAPIClient(self.picAPIURL)
        """testing for XML output""" 
        
        userInfo = {'title':'test_title', 'workurl':'test_work_url', 'type':'test_type', 'year':'test_year', 'description':'test_desc', 'creator':'test_creator', 'holder':'test_holder', 'outputType':'xml'}               
        output2 = picserver.getLicense('pic_cc_by', userInfo)
        tree = lxml.etree.parse(StringIO(output2))
        root = tree.getroot()
        self.failUnlessEqual(root.tag, "result")
        
    def test_configurationReader(self):
        # instantiating config file reader
        configFilesPath = settings.PICBADGEPATH + '/configFiles/'
        configFile = "testConfigFile.txt"  
        agreeFile = "testAgreement.txt"      
        
        reader = configReader(configFilesPath, configFile)
        appConfig = reader.getConfigHandler()
        book1Config = appConfig.book1
        book1Choices = reader.getChoices(book1Config)
        book1Name = book1Config.name
        
        # this part tests including another config file in main config
        book2Config = appConfig.otherBook.book2
        book2Choices = reader.getChoices(book2Config)
        book2Name = book2Config.name
        
        # this part tests reading a text block from another file
        agreeText = reader.getAgreement(agreeFile)
        # this part tests including choices from another file.
        booksList = appConfig.booknames
        
        self.failUnlessEqual(book1Name, "My book 1")
        self.failUnlessEqual(book1Choices, [('2009', '2009'), ('2007', '2007')])
        
        self.failUnlessEqual(book2Name, "My book 2")
        self.failUnlessEqual(book2Choices, [('2019', '2019'), ('2017', '2017')])
        
        self.failUnlessEqual(agreeText.strip(), "My test agreement.")       
        
        """ write code for template testing """ 
    


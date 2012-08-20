"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.conf import settings
import urllib2

class picBadgeAPITests(TestCase):
    
    picAPIURL = settings.PICBADGEAPI_URL + "/" + settings.PICBADGEAPI_PATH
    
    def test_getLicenses(self):
        strPath = self.picAPIURL + "/licenses/"
        req = urllib2.Request(strPath)
        response = urllib2.urlopen(req)
        expectedOutput = '<?xml version="1.0" ?><licenses><license id="pic_cc_zero">PIC CC ZERO Waiver</license><license id="pic_cc_by">PIC CC BY License</license></licenses>'
        self.failUnlessEqual(response.read(), expectedOutput)
        
    def test_getPicZeroFields(self):
        strPath = self.picAPIURL + "/licenses/pic_cc_zero/"
        req = urllib2.Request(strPath)
        response = urllib2.urlopen(req)
        expectedOutput = '<?xml version="1.0" ?><licenseClass id="pic_cc_zero"><field id="attribution_url"><label>Your URL</label><description>The URL of the work</description></field><field id="territory"><label>Territory</label><description>The country code</description></field><field id="creator"><label>Publisher</label><description>The name of the creator of the work</description></field><field id="outputType"><description>The format of the output</description><label>License Output format</label><label>XML having License HTML and RDF</label><label>License HTML ONLY</label></field><field id="title"><label>Title of Work</label><description>The title of the work</description></field></licenseClass>'
        self.failUnlessEqual(response.read(), expectedOutput)
        
    def test_getPicCCByFields(self):
        strPath = self.picAPIURL + "/licenses/pic_cc_by/"
        req = urllib2.Request(strPath)
        response = urllib2.urlopen(req)
        expectedOutput ='<?xml version="1.0" ?><licenseClass id="pic_cc_by"><field id="description"><label>Description</label><description>A brief description of the work</description></field><field id="creator"><label>Attribute work to name</label><description>The name of the creator of the work</description></field><field id="holder"><label>Holder</label><description>The name of the work holder</description></field><field id="title"><label>Title of Work</label><description>The title of the work</description></field><field id="outputType"><description>The format of the output</description><label>License Output format</label><label>XML having License HTML and RDF</label><label>License HTML ONLY</label></field><field id="year"><label>Year</label><description>The year in which the work was produced</description></field><field id="type"><label>Format of Work</label><description>The format of the work</description></field><field id="workurl"><label>Attribute work to URL</label><description>The URL of the work</description></field></licenseClass>'
        self.failUnlessEqual(response.read(), expectedOutput)
        
    
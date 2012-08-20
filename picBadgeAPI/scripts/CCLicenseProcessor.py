# Author:	Azhar Sikander
# This file contains CCLicenseProcessor class that contains modules
# to process Creative Commons's generated license.

import sys
import traceback
import re
import xml.dom.minidom
import lxml.etree
from StringIO import StringIO

class CCLicenseProcessor:
	licenseType = ""
	
	def setLicenseType(self, aLicenseType):
		self.licenseType = aLicenseType
		
	def getLicenseType(self):
		return licenseType
		
	"""CC Licenses Processor class"""
		# embed PIC LOGO into CC returned license to make it PIC CC License
	def embeddPICLOGO(self, prmlicenseXML):
		RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
		CC_NAMESPACE = "http://creativecommons.org/ns#"
		DC_NAMESPACE = "http://purl.org/dc/elements/1.1/"
		DCT_NAMESPACE = "http://purl.org/dc/terms/"
		
		RDF = "{%s}" % RDF_NAMESPACE
		CC = "{%s}" % CC_NAMESPACE
		DC = "{%s}" % DC_NAMESPACE
		DCT = "{%s}" % DCT_NAMESPACE
	
		NSMAP = {
				None : CC_NAMESPACE, # the default namespace (no prefix) 
				'rdf': RDF_NAMESPACE,
				'dc' : DC_NAMESPACE, 				 
		} 
		# Added second map because XPath complain about a blank namespace entry "None"
		DCNSMAP = {
				'dc' : DC_NAMESPACE, 				 
		} 
		DCTNSMAP = {
				'dct' : DCT_NAMESPACE, 				 
		}
		
		doc = lxml.etree.parse(StringIO(prmlicenseXML))		
		
		###Extend the requires and permits section of the license ####
		licenseSectionElem = doc.getroot().find("licenserdf")
		
		rdfDescElem1 = lxml.etree.Element(RDF + "Description", nsmap=NSMAP)		
		rdfDescElem1.set(RDF + "about", "dc:contributor");
		rdfRequiresElem1 = lxml.etree.SubElement(rdfDescElem1, "requires")		
		rdfRequiresElem1.set(RDF + "resource", "http://www.polarcommons.org/ethics-and-norms-of-data-sharing.php");
		licenseSectionElem.append(rdfDescElem1)	
		
		rdfDescElem2 = lxml.etree.Element(RDF + "Description", nsmap=NSMAP)		
		rdfDescElem2.set(RDF + "about", "dc:audience");
		rdfRequiresElem2 = lxml.etree.SubElement(rdfDescElem2, "requires")		
		rdfRequiresElem2.set(RDF + "resource", "http://www.polarcommons.org/ethics-and-norms-of-data-sharing.php");
		licenseSectionElem.append(rdfDescElem2)	
				
		###Generating PIC LOGO to embedd in CC License####
		licenseHTML = doc.getroot().find("html")
		
		piclogoElem = lxml.etree.Element("a")
		
		piclogoElem.set("href", "http://polarcommons.org/ethics-and-norms-of-data-sharing.php")
		
		picimgElem = lxml.etree.SubElement(piclogoElem, "img")
		picimgElem.set("src", "http://polarcommons.org/images/PIC_print_small.png")
		altText = "Polar Information Commons's %s."
		if (self.licenseType == "by") :
			altText = altText % "PICCCBY license"
		elif (self.licenseType == "zero") :
			altText = altText % "PICCC0 waver"
		else:
			raise "Internal error: unknown license type specified."
		
		picimgElem.set("alt", altText)
		
		####################################
		
		if licenseHTML[0].tag == "p":
			licenseHTML[0].insert(0, piclogoElem)
		else:
			licenseHTML.insert(0, piclogoElem)		
		
		
		### Customize license text ###
		find = lxml.etree.XPath("//dc:creator", namespaces = DCNSMAP)
		creator = find(doc.getroot())
		
		# Remove all whitespace around title entries
		find = lxml.etree.XPath("//dct:title", namespaces = DCTNSMAP)
		try:
			titles = find(doc.getroot())
			for title in titles:
				title.text = title.text.trim() 
		except Exception, e:
				print traceback.print_exc()			
		
		
		creatorText = " <span>%s expects that users will follow the " % creator[0].text 
		linkHref = "<a rel=\"cc:useGuidelines\" href=" + '"http://polarcommons.org/ethics-and-norms-of-data-sharing.php">'
		linkText = "Polar Information Commons Ethics and Norms of Data Sharing" + "</a>.</span>"
		normsText = creatorText + linkHref + linkText
		
		if licenseHTML[0].tag == "p":
			licenseParagraph = licenseHTML.find("p")			
			
			try:
				paragraphText = lxml.etree.tostring(licenseParagraph)
				 
				publishTextMatch = re.search(r'This work is published from\W*(<span[\W\w^>]*>[\w\W]*?</span>)\s*\.\s*', paragraphText) 
				publishText = "<span>This work is published from " + publishTextMatch.group(1).strip() + ".</span>"
				newParagraphText = re.sub(r'(This work is published from\W*<span[\W\w^>]*>[\w\W]*?</span>\s*\.\s*)?', r"", paragraphText)		
				paragraphInnerText = r"<p\1" + normsText + "  "+ publishText + "</p>"
				newParagraphText = re.sub(r'<p([\W\w^>]*>[\w\W]*?)</p>', paragraphInnerText, newParagraphText)
				newParagraphText = re.sub(r'\s*</span>', '</span>', newParagraphText)
				newLicenseParagraph = lxml.etree.fromstring(newParagraphText)
												
				#newLicenseParagraph.append(publishElem)
				
				licenseHTML.replace(licenseParagraph, newLicenseParagraph)
			except Exception, e:
				print traceback.print_exc()	
		else:
			try:
				licenseHTMLText = lxml.etree.tostring(licenseHTML)							
				newLicenseHTMLText = re.sub(r'<html>([\w\W]*?)</html>', r"<html><p>\1 " + normsText + "</p></html>", licenseHTMLText)
				newLicenseHTML = lxml.etree.fromstring(newLicenseHTMLText)
				doc.getroot().replace(licenseHTML, newLicenseHTML)
			except Exception, e:
				print traceback.print_exc()
				
		return lxml.etree.tostring(doc, pretty_print=True)
				
	# extracts license HTML from CC returned license XML
	def extractLicenseHTML(self, prmLicenseXML):
		doc = lxml.etree.parse(StringIO(prmLicenseXML))		
		licenseHTML = doc.getroot().find("html")
		
		return lxml.etree.tostring(licenseHTML, pretty_print=True)
	

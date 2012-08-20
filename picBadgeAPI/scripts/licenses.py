# Author:	Azhar Sikander
# This file contains all information about ALL the PIC CC Licenses.
import sys
import re
from xml.dom.minidom import Document
from django.conf import settings
from polarCommonProj.picBadge.scripts.utilityFunctions import Callable
from polarCommonProj.picBadge.configurationReader import configReader

# I don't necessarily like using the Web App's config, but I don't really
# want to duplicate it either, so I'll just do this for now
configFilesPath = settings.PICBADGEPATH + '/configFiles/'
configFile = "picBadgeAppConfiguration.cfg"
CC_Zero_AgreementFile = 'ccLicAgreement.txt'
CC_By_AgreementFile = 'ccByLicAgreement.txt'

reader = configReader(configFilesPath, configFile)
appConfig = reader.getConfigHandler()

class picLicenses:
	
	# the api offers two differnt output types
	licenseOutput = {"html": "License HTML ONLY", "xml":"XML having License HTML and RDF"}
	# pic cc license classes
	picLicenseClasses = {'pic_cc_zero':"PIC CC ZERO Waiver", 'pic_cc_by':"PIC CC BY License"}
	# pic_cc_zero license specifications... fields, labels and descriptions
	picCCZeroFields = {'title': ("Title of Work", "The title of the work"),
						'attribution_url':("Your URL", "The URL of the work"),
						'territory':("Territory", "The country code"),
						'creator':("Publisher", "The name of the creator of the work"),
						'outputType':("License Output format", "The format of the output")}
	
	# pic_cc_by license specifications... fields, labels and descriptions
    # Ticket 181 -- removed 'sourceurl':("Source work URL", "The URL of the work source"),
	picCCByFields = {'title': ("Title of Work", "The title of the work"),
						'workurl':("Attribute work to URL", "The URL of the work"),						
						'type':("Format of Work", "The format of the work"),
						'year':("Year", "The year in which the work was produced"),
						'description':("Description", "A brief description of the work"),
						'creator':("Attribute work to name", "The name of the creator of the work"),
						'holder':("Holder", "The name of the work holder"),
						'outputType':("License Output format", "The format of the output")}
	
	# Returns PIC_CC License Classes in XML format
	def getLicenseClasses(self):
		doc = Document()
		# create root node "licenses"
		licenses = doc.createElement("licenses")
		doc.appendChild(licenses)
		# for each license, create a subnode "license" with id = license_id .. and name as text.
		for license in self.picLicenseClasses:
			licenseNode = doc.createElement("license")
			licenseNode.setAttribute("id", license)
			# add license name as text
			textNode = doc.createTextNode(self.picLicenseClasses[license])
			licenseNode.appendChild(textNode)
			licenses.appendChild(licenseNode)		
		
		return doc.toxml()	
	
	# Returns Territories in XML Format
	def getTerritories(self):
		doc = Document()
		
		#create root node "territories"
		territories = doc.createElement("territories")
		doc.appendChild(territories)
		
		territoryConfig = appConfig.picZeroForm.pic_cc_zero.territory
		countries = reader.getChoices(territoryConfig)
		for country in countries:
			countryNode = doc.createElement('territory')
			countryNode.setAttribute('code', country[0]);
			countryText = doc.createTextNode(country[1])
			countryNode.appendChild(countryText)
			territories.appendChild(countryNode)
		
		return doc.toxml()
	
	# Returns License Agreement in XML Format
	def getLicenseAgreement(self, license):
		doc = Document()
		
		licenseRoot = doc.createElement("licenseAgreement")
		doc.appendChild(licenseRoot)
		licenseText = '';
		
		if license == 'pic_cc_zero':
			licenseText = reader.getAgreement(CC_Zero_AgreementFile)
		else:
			licenseText = reader.getAgreement(CC_By_AgreementFile)
		licenceNode = doc.createTextNode(licenseText);
		licenseRoot.appendChild(licenceNode)
		
		return doc.toxml()
	
	#return a particular license's attributes
	def getLicenseAttributes(self, license):
		# if license is not found... return error
		if not license in self.picLicenseClasses:
			raise AttributeError
		
		doc = Document()
		licenseClass = doc.createElement("licenseClass")
		licenseClass.setAttribute("id", license)
		doc.appendChild(licenseClass)
		
		# get fields of the specified license.
		fieldsDict = {}
		if license == "pic_cc_zero":
			fieldsDict = self.picCCZeroFields
		elif license == "pic_cc_by":
			fieldsDict = self.picCCByFields
		
		# for each attribute in the license, create field node with an attribute "id" and two sub nodes "label" and "description".
		for field in fieldsDict:
			fieldNode = doc.createElement("field")
			fieldNode.setAttribute("id", field)
			
			labelNode = doc.createElement("label")
			textNode = doc.createTextNode(fieldsDict[field][0])
			labelNode.appendChild(textNode)
			
			descriptionNode = doc.createElement("description")
			textNode = doc.createTextNode(fieldsDict[field][1])
			descriptionNode.appendChild(textNode)
			
			fieldNode.appendChild(labelNode)
			fieldNode.appendChild(descriptionNode)
			
			# adding outputType.. it has two extra parameters "type" and "enum"
			if field == "outputType":
				typeNode = doc.createElement("type")
				textNode = doc.createTextNode("enum")
				typeNode.appendChild(textNode)
				fieldNode.appendChild(labelNode)
				
				for otype in self.licenseOutput:
					enumNode = doc.createElement("enum")
					enumNode.setAttribute("id", otype)
			
					labelNode = doc.createElement("label")
					textNode = doc.createTextNode(self.licenseOutput[otype])
					labelNode.appendChild(textNode)
					fieldNode.appendChild(labelNode)
					
			licenseClass.appendChild(fieldNode)				
				
		return doc.toxml()
		

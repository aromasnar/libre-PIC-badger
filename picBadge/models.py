# Author:	Azhar Sikander
# This file contains form specifications of all the forms in the badging application.

from django.db import models
from django import forms
from polarCommonProj.picBadge.scripts.utilityFunctions import Utilities
import config
import os.path
from django.conf import settings
from symbol import except_clause
from polarCommonProj.picBadge.configurationReader import configReader 

# instantiating config file reader
configFilesPath = settings.PICBADGEPATH + '/configFiles/'
configFile = "picBadgeAppConfiguration.cfg"
CC_Zero_AgreementFile = 'ccLicAgreement.txt'
CC_By_AgreementFile = 'ccByLicAgreement.txt'

reader = configReader(configFilesPath, configFile)
appConfig = reader.getConfigHandler()
	
# Badging API requires output type for both licenses (pic_cc_by & pic_cc_zero) and have following two values.
outputTypeConfig = appConfig.picBadgerAppOutputType
outputTypeChoices = reader.getChoices(outputTypeConfig)
 
# Label for license Agreement ... NOTE:  DONT CHANGE
licenseAgreementLabel = "Agreement"

# Form specification for the PIC CC Zero form w.r.t PIC CC Zero specification provided by pic api.
class cc0UserInfoForm(forms.Form):
    #global reader, CC_Zero_AgreementFile	
    titleConfig = appConfig.picZeroForm.pic_cc_zero.title
    title = forms.CharField(required=False, label=titleConfig.label, help_text=titleConfig.helpText)
	
    attrURLConfig = appConfig.picZeroForm.pic_cc_zero.attributionURL
    attribution_url = forms.CharField(label=attrURLConfig.label, help_text=attrURLConfig.helpText)
	
    territoryConfig = appConfig.picZeroForm.pic_cc_zero.territory
    countries = reader.getChoices(territoryConfig)        
    territory = forms.ChoiceField(label=territoryConfig.label, choices=countries, help_text=territoryConfig.helpText, initial = reader.getInitial(territoryConfig))

    creatorConfig = appConfig.picZeroForm.pic_cc_zero.creator
    creator = forms.CharField(label=creatorConfig.label, help_text=creatorConfig.helpText)
	    
    outputType = forms.ChoiceField(label=outputTypeConfig.label, choices=outputTypeChoices, help_text=outputTypeConfig.helpText, initial = reader.getInitial(outputTypeConfig))
    
    agreementconfirm = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':60}), initial=reader.getAgreement(CC_Zero_AgreementFile), label=licenseAgreementLabel)
    agreementconfirm.widget.attrs['readonly'] = True
	
# Form specification for the PIC CC By form w.r.t PIC CC By specification provided by pic api.
class ccByUserInfoForm(forms.Form):
	#global reader, CC_By_AgreementFile
	titleConfig = appConfig.picCCByForm.pic_cc_by.title
	title = forms.CharField(required=False, label=titleConfig.label, help_text = titleConfig.helpText) 
	
	workurlConfig = appConfig.picCCByForm.pic_cc_by.workURL
	workurl = forms.CharField(required=True, label=workurlConfig.label, help_text = workurlConfig.helpText)
	
	# JLL Removed for ticket 181 
	# sourceurlConfig = appConfig.picCCByForm.pic_cc_by.sourceURL
	# sourceurl = forms.CharField(required=False, label=sourceurlConfig.label, help_text=sourceurlConfig.helpText)
	
	typeConfig = appConfig.picCCByForm.pic_cc_by.type
	workTypeChoices = reader.getChoices(typeConfig)
	type = forms.ChoiceField(required=True, label=typeConfig.label, choices = workTypeChoices, help_text = typeConfig.helpText, initial = reader.getInitial(typeConfig))	
	
	yearConfig = appConfig.picCCByForm.pic_cc_by.year
	year = forms.CharField(required=False, label=yearConfig.label, help_text = yearConfig.helpText)
	
	descriptionConfig = appConfig.picCCByForm.pic_cc_by.description
	description = forms.CharField(widget=forms.widgets.Textarea(attrs={'rows':4, 'cols':60}) , required=False, label=descriptionConfig.label, help_text = descriptionConfig.helpText)
	#description = forms.Textarea(rows = 5, required=False, label=descriptionConfig.label, help_text = descriptionConfig.helpText)
	creatorConfig = appConfig.picCCByForm.pic_cc_by.creator
	creator = forms.CharField(required=False, label=creatorConfig.label, help_text = creatorConfig.helpText) 
	
	holderConfig = appConfig.picCCByForm.pic_cc_by.holder
	holder = forms.CharField(required=False, label=holderConfig.label, help_text = holderConfig.helpText)	
	
	outputType = forms.ChoiceField(label=outputTypeConfig.label, choices=outputTypeChoices, help_text=outputTypeConfig.helpText, initial = reader.getInitial(outputTypeConfig))
	
	agreementconfirm = forms.CharField(widget=forms.Textarea(attrs={'rows':10, 'cols':60}), initial=reader.getAgreement(CC_By_AgreementFile), label=licenseAgreementLabel)
	agreementconfirm.widget.attrs['readonly'] = True

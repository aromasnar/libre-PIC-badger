# Author:	Azhar Sikander
# This file contains all the views for the badging application.
			
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.http import Http404
from django.http import HttpResponse
from django.forms import ModelForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail



from org.nsidc.libre.datacaster.DataCast import DataCast
from org.nsidc.libre.datacaster.DataCast import DataCastFactory
from org.nsidc.libre.datacaster.Util import NETWORKTools
from org.nsidc.libre.datacaster.GCMDParameter import Parameters
from org.nsidc.libre.datacaster.Util import FileWriter
from org.nsidc.libre.datacaster.GCMDLocation import Location
from org.nsidc.libre.datacaster.GCMDLocation import Locations
from org.nsidc.libre.datacaster.CreateiveCommonsLicense import CCApplication
from org.nsidc.libre.datacaster.CreateiveCommonsLicense import CCRestAPI
from org.nsidc.libre.datacaster.DBTools import GCMD_Param_Loader
from org.nsidc.libre.datacaster.DBTools import DBQuery
from org.nsidc.libre.datacaster.DataCaster import DataCaster


TEMP_DIR=getattr(settings, "DC_TEMP_DIR", "default_foo")
DC=DataCaster(TEMP_DIR)


# This view creates the main page of the badging app. 
def index(request):		
	
	# Dynamically create the badging app's main page using the two form objects.
	return render_to_response('datacaster_template.html',{})	



###########################################################################
# Save-Cast Service Handler
###########################################################################
"""
This method saves a Data-Cast posted by a suer to a temp file.
The relative url to the temp file is returned to the client.

In this implementation, the url is passed to the client-side JavaScript callback function (saveCastCallback)
which opens tries to open ane/or save the file.

"""

@csrf_exempt
def save_cast(request):
        rid=request.POST['rid']
        xml=request.POST['value']
        response=DC.saveCast(xml, rid)
        return HttpResponse(xml, mimetype='application/xml')

###########################################################################
# Download Cast
###########################################################################
"""
Opens and returns a cast file with a particular mimetype.
"""

def fetch_cast(request,cast_name):
        file=open(TEMP_DIR+cast_name + ".xml");
        return HttpResponse(file, mimetype='application/nsidc-datacast')


    
    
###########################################################################
# Load-Cast Service Handler
###########################################################################
"""
This method transforms a Data-Cast XML file (uploaded by the user)
into the JSON format used by the Data-Cast Widget.
"""
@csrf_exempt
def load_cast(request):
        if request.method == 'POST':
                file = request.FILES['uploadFormElement']
                json=DC.loadCastFromFile(file)
                return HttpResponse(json)
        return HttpResponse('Was not expecting that...')
    
    
###########################################################################
# Load-Cast from URL Handler
###########################################################################
"""
This method fetches a Data-Cast XML file from a URL.
"""

def load_cast_from_url(request):
        json=DC.loadCastFromURL("http://3rdflatiron.com/cast_jess-test.xml")
        return HttpResponse(json)

###########################################################################
# Publish and EMAIL Data-Cast
###########################################################################

@csrf_exempt
def pub_cast_email(request):

        xml=request.POST['xml']
        link=request.POST['link']
        title=request.POST['title']
        email=request.POST['email']

        #EMAIL Message Body
        email_message ="-----------------------\n"
        email_message+="-----------------------\n"
        email_message+="This message was generated at your request by the by the Libre: Data-Casting tool.\n\n"
        email_message+="Libre:Data-Cast\n"
        email_message+="Title:" + title + "\n"
        email_message+="Link:" + link   + "\n"
        email_message+="\n\n"
        email_message+=xml

        #Send the EMAIL
        send_mail('Data-Cast', email_message, 'youremail@yourdomain.com',[email], fail_silently=False)
        return HttpResponse('{"status":"OK"}')


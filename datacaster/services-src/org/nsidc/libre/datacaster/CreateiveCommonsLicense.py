"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

import libxml2
import urllib
import urllib2


"""
This class models a Creative Commons Licens Application.
"""

class CCApplication:

    def __init__(self):
        self.locale=None

#Locale
    def setLocale(self,locale):
        self.locale=locale

    def getLocale(self):
        return self.locale
#Title
    def setTitle(self,title):
        self.title=title

    def getTitle(self):
        return self.title
#Work Url
    def setWorkUrl(self,workUrl):
        self.workUrl=workUrl

    def getWorkUrl(self):
        return self.workUrl
#Source Url
    def setSourceUrl(self,sourceUrl):
        self.sourceUrl=sourceUrl

    def getSourceUrl(self):
        return self.sourceUrl
#Description
    def setDescription(self,description):
        self.description = description

    def getDescription(self):
        return self.description

#Creator
    def setCreator(self,creator):
        self.creator=creator
    def getCreator(self):
        return self.creator
#Holder
    def setHolder(self,holder):
        self.holder=holder
    def getHolder(self):
        return self.holder
#Type
    def setType(self,type):
        self.type=type
    def getType(self):
        return self.type
#Year
    def setYear(self,year):
        self.year=year
    def getYear(self):
        return self.year

#Commercial
    def setCommercial(self,commercial):
        self.commercial=commercial
    def getCommercial(self):
        return self.commercial
#Derivitrives
    def setDerivitives(self,derivitives):
        self.derivitives=derivitives

    def getDerivitives(self):
        return self.derivitives

#Jurisdiction
    def setJurisdiction(self,jurisdiction):
        self.jurisdiction=jurisdiction
    def getJurisdiction(self):
        return self.jurisdiction

    def __str__(self):


        apps ="LOCALE        :" + self.getLocale()          + "\n"

        apps+="COMMERCIAL    :" + self.getCommercial()      + "\n"

        apps+="DERIVITIVES   :" + self.getDerivitives()     + "\n"

        apps+="JURSDICTION   :" + self.getJurisdiction()    + "\n"

        apps+="TITLE         :" + self.getTitle()           + "\n"

        apps+="WORK-URL      :" + self.getWorkUrl()         + "\n"

        apps+="SOURCE-URL    :" + self.getSourceUrl()       + "\n"

        apps+="TYPE          :" + self.getType()            + "\n"

        apps+="YEAR          :" + self.getYear()            + "\n"

        apps+="DESCRIPTION   :" + self.getDescription()     + "\n"

        apps+="CREATOR       :" + self.getCreator()         + "\n"

        apps+="HOLDER        :" + self.getHolder()          + "\n"


        return apps

    def getAnswers(self,format=False):

        if(format==False):
            answers  ="<answers>"
            answers +="<locale>"            +self.getLocale()       +"</locale>"
            answers +="<license-standard>"
            answers +="<commercial>"        +self.getCommercial()   +"</commercial>"
            answers +="<derivatives>"       +self.getDerivitives()  +"</derivatives>"
            answers +="<jurisdiction>"      +self.getJurisdiction() +"</jurisdiction>"
            answers +="</license-standard>"
            answers +="<work-info>"
            answers +="<title>"             +self.getTitle()        +"</title>"
            answers +="<work-url>"          +self.getWorkUrl()      +"</work-url>"
            answers +="<source-url>"        +self.getSourceUrl()    +"</source-url>"
            answers +="<type>"              +self.getType()         +"</type>"
            answers +="<year>"              +self.getYear()         +"</year>"
            answers +="<description>"       +self.getDescription()  +"</description>"
            answers +="<creator>"           +self.getCreator()      +"</creator>"
            answers +="<holder>"            +self.getHolder()       +"</holder>"
            answers +="</work-info>"
            answers +="</answers>"

        if(format==True):
            answers  ="<answers>\n"

            answers +="  <locale>"              +self.getLocale()       +"</locale>\n"
            answers +="  <license-standard>"
            answers +="    <commercial>"        +self.getCommercial()   +"</commercial>\n"
            answers +="    <derivatives>"       +self.getDerivitives()  +"</derivatives>\n"
            answers +="    <jurisdiction>"      +self.getJurisdiction() +"</jurisdiction>\n"
            answers +="  </license-standard>\n"
            answers +="  <work-info>\n"
            answers +="    <title>"              +self.getTitle()        +"</title>\n"
            answers +="    <work-url>"           +self.getWorkUrl()      +"</work-url>\n"
            answers +="     <source-url>"        +self.getSourceUrl()    +"</source-url>\n"
            answers +="     <type>"              +self.getType()         +"</type>\n"
            answers +="     <year>"              +self.getYear()         +"</year>\n"
            answers +="     <description>"       +self.getDescription()  +"</description>\n"
            answers +="     <creator>"           +self.getCreator()      +"</creator>\n"
            answers +="     <holder>"            +self.getHolder()       +"</holder>\n"
            answers +="  </work-info>\n"

            answers +="</answers>"

        return answers

def getAttribute(element,name):
    for p in element.properties:
        if(p.type=='attribute'):
            if(p.name==name):
                return p.content
            

class CCRestAPI:

    def getLicense(self,ccApplicationAnswersXML):
        baseurl='http://api.creativecommons.org/rest/1.5/license/ddd/issue'
        #baseurl='http://api.creativecommons.org/rest/1.5'
        #baseurl='http://api.creativecommons.org/rest/dev/license/by/issue'
        values={'answers':ccApplicationAnswersXML}
        data=urllib.urlencode(values)
        req=urllib2.Request(baseurl,data)
        response=urllib2.urlopen(req)
        result=response.read()
        return result

    def parseLicense(self,xml):

        doc=libxml2.parseFile("/home/anderson/xml/cc.xml")

        dcNs = doc.xpathNewContext()
        dcNs.xpathRegisterNs('dc', "http://purl.org/dc/elements/1.1/")

        rdfNs = doc.xpathNewContext()
        rdfNs.xpathRegisterNs('rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
            
#xmlns="http://creativecommons.org/ns#"
#xmlns:dc="http://purl.org/dc/elements/1.1/"
#xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"

        print doc
        print "\n\n----------"

        uri=doc.xpathEval("//result/license-uri")[0].content

        name=doc.xpathEval("//result/license-name")[0].content

        html=doc.xpathEval("//result/html")[0]
        
        title=dcNs.xpathEval("//dc:title")[0].content

        type=dcNs.xpathEval("//dc:type")[0]
        type=getAttribute(type,'resource')

        source=dcNs.xpathEval("//dc:source")[0]
        source=getAttribute(source,'resource')

        date=dcNs.xpathEval("//dc:date")[0].content

        description=dcNs.xpathEval("//dc:description")[0].content

        creator=dcNs.xpathEval("//dc:creator")[0].content.strip()

        rights=dcNs.xpathEval("//dc:rights")[0].content.strip()
        

        print "title:           "           + title
        print "type:            "           + type
        print "date:            "           + date
        print "description:     "           + description
        print "creator          "           + creator
        print "rights           "           + rights
        print "source           "           + source
        print "uri:             "           + uri
        print "name:            "           + name
        print  html
       
        
        
        
        
     

        

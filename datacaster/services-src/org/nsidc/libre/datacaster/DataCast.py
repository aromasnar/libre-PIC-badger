"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

import libxml2
import GCMDParameter
from Contact import Contact

class DataCast:

    def setContats(self,contacts):
        self.contacts=contacts
        
    def getContacts(self):
        return self.contacts

    def get_gcmd_params(self):
        return self.gcmdParams

    def set_gcmd_params(self,gcmdParams):
        self.gcmdParams=gcmdParams

    def getRid(self):
        return self.rid
    def getTitle(self):
        return self.title
    def getProgress(self):
        return self.progress
    def getLanguage(self):
        return self.language
    def getSummary(self):
        return self.summary
    def getCreator(self):
        return self.creator
    def getReleaseDate(self):
        return self.releaseDate
    def getReleasePlace(self):
        return self.releasePlace
    def getPublisher(self):
        return self.publisher
    def getVersion(self):
        return self.version
    def getOnlineResource(self):
        return self.onlineResource

    def setRid(self,rid):
        self.rid=rid
    def setTitle(self,title):
        self.title=title
    def setProgress(self,progress):
        self.progress=progress
    def setLanguage(self,language):
        self.language=language
    def setSummary(self,summary):
        self.summary=summary
    def setCreator(self,creator):
        self.creator=creator
    def setReleaseDate(self,date):
        self.releaseDate=date
    def setReleasePlace(self,place):
        self.releasePlace=place
    def setPublisher(self,publisher):
        self.publisher=publisher
    def setVersion(self,version):
        self.version=version
    def setOnlineResource(self,url):
        self.onlineResource=url

    def __str__(self):
        return "DATACAST ..."

    def asJSON(self):

        json='{'
        json+='casts:['
        json+='{'
        json+='"rid":"'+self.getRid()+'",'
        json+='"title":"'+self.getTitle()+'",'
        json+='"progress":"'+self.getProgress()+'",'
        json+='"summary":"'+self.getSummary()+'",'
        json+='"language":"'+self.getLanguage()+'",'
        json+='"creator":"'+self.getCreator()+'",'
        json+='"release_date":"'+self.getReleaseDate()+'",'
        json+='"release_place":"'+self.getReleasePlace()+'",'
        json+='"publisher":"'+self.getPublisher()+'",'
        json+='"version":"'+self.getVersion()+'",'
        json+='"online_resource":"'+self.getOnlineResource()+'",'
        json+='\n"contacts":['
        for c in self.getContacts():
            json+="\n          " + c.asJSON() + ","
        json+='\n          ],'
        json+='\n"gcmd_parameters":['
        for p in self.get_gcmd_params():
            json+="\n      "     + p.as_json() + ","
        json+='\n]'
        json+='}'
        json+=']'
        json+='}'

        return json


class XMLCastTool:
    def __init__(self,xmlfile):
        self.doc=libxml2.parseFile(xmlfile)


    def getContactInfo(self):

        contactList=[]

        contacts=self.doc.xpathEval("//contact_info/contact")

        for contact in contacts:

            type=contact.xpathEval("contact-type")[0].content
            firstName=contact.xpathEval("first_name")[0].content
            lastName=contact.xpathEval("last_name")[0].content
            institute=contact.xpathEval("institute")[0].content

            p=Contact()
            p.setFirstName(firstName)
            p.setLastName(lastName)
            p.setInstitute(institute)
            p.setType(type)

            contactList.append(p)

            

        return contactList

    def getGCMDParams(self):

        paramList=[]

        params=self.doc.xpathEval("//science_keywords/gcmd_parameter")

        for param in params:
            cat=param.xpathEval("category")[0].content
            topic=param.xpathEval("topic")[0].content
            term=param.xpathEval("term")[0].content

            gcmdParam=GCMDParameter.Parameter()
            gcmdParam.setCat(cat)
            gcmdParam.setTopic(topic)
            gcmdParam.setTerm(term)

            try:
                level=param.xpathEval("level_0")[0].content
                gcmdParam.addLevel(level)
            except:
                pass
            try:
                level=param.xpathEval("level_1")[0].content
                gcmdParam.addLevel(level)
            except:
                pass
            try:
                level=param.xpathEval("level_2")[0].content
                gcmdParam.addLevel(level)
            except:
                pass
            try:
                level=param.xpathEval("level_3")[0].content
                gcmdParam.addLevel(level)
            except:
                pass

            #print gcmdParam.as_json()
            paramList.append(gcmdParam)

        return paramList
            


    def getElementValue(self,element_name):

        try:
            value=self.doc.xpathEval(element_name)[0].content
            return value
        except:
            return ""


class DataCastFactory:

    def castFromXML(self,cast_xml_file):

        xml=XMLCastTool(cast_xml_file)

        rid         =xml.getElementValue("//general_info/resource_id")
        title       =xml.getElementValue("//general_info/title")
        creator     =xml.getElementValue("//general_info/creator")
        place       =xml.getElementValue("//general_info/place")
        version     =xml.getElementValue("//general_info/version")
        publisher   =xml.getElementValue("//general_info/publisher")
        summary     =xml.getElementValue("//general_info/summary")
        url         =xml.getElementValue("//general_info/online_resource")
        progress    =xml.getElementValue("//general_info/progress")
        language    =xml.getElementValue("//general_info/language")
        date        =xml.getElementValue("//general_info/release_date")

        gcmdKeywords=xml.getGCMDParams()

        contacts=xml.getContactInfo()

        
            
            

        cast=DataCast()
        
        cast.setCreator(creator)
        cast.setLanguage(language)
        cast.setOnlineResource(url)
        cast.setProgress(progress)
        cast.setPublisher(publisher)
        cast.setReleasePlace(place)
        cast.setRid(rid)
        cast.setSummary(summary)
        cast.setVersion(version)
        cast.setTitle(title)
        cast.setReleaseDate(date)
        cast.set_gcmd_params(gcmdKeywords)
        cast.setContats(contacts)
        
        return cast
        
        
        #cast.setReleaseDate()









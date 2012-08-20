"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

from DataCast import DataCastFactory
from Util import NETWORKTools
from Util import FileWriter

class DataCaster:

    def __init__(self,temp_dir="/tmp/"):

        self.temp_dir=temp_dir

        pass


    #Load Data-Cast from URL
    def loadCastFromURL(self,url="http://3rdflatiron.com/cast_jess-test.xml"):
        castf=DataCastFactory()
        file=NETWORKTools().fetchDataFromURL2File(url, self.temp_dir + "tmp.xml")
        cast=castf.castFromXML(file)
        json=cast.asJSON()
        return json

    #Load Data-Cast from file uploaded by user.
    def loadCastFromFile(self,file):
        xml=file.read()
        writer=FileWriter(self.temp_dir + "temp_cast_2.xml" )
        writer.writeLine(xml)
        writer.close()
        castf=DataCastFactory()
        cast=castf.castFromXML(self.temp_dir+"temp_cast_2.xml")
        json=cast.asJSON()
        return json

    #Save Cast to Temp File
    def saveCast(self,cast_xml,cast_rid):
        print cast_rid
        writer=FileWriter(self.temp_dir + "cast_" + cast_rid + ".xml" )
        writer.writeLine(cast_xml)
        return "/tmp/cast_" + cast_rid + ".xml"



    


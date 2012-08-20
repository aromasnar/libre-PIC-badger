"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

import urllib2

class FileWriter:
    def __init__(self,file_path):
        self.file_path=file_path
        self.file=open(self.file_path,'w')
        #print "Opening File"

    def writeLine(self,line):
        self.file.write(line + "\n")

    def __del__(self):
        self.file.close()

    def close(self):
        self.__del__()

    def get_file(self):
        return self.file
    


class NETWORKTools:


    def fetchDataFromURL2File(self,url,file):
        try:
            data=self.fetchDataFromURL(url)
            fileWriter=FileWriter(file)
            fileWriter.writeLine(data)
            fileWriter.close()
            return file

        except:
            return "COULD NOT CONNECT TO URL:" + url

    def fetchDataFromURL(self, url):
       try:
            usock = urllib2.urlopen(url)
            data = usock.read()
            value=data.strip()
            usock.close()
            return value
       except:
           return "COULD NOT CONNECT TO URL:" + url





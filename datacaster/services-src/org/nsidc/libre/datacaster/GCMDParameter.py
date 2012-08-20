"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

from Util import NETWORKTools
from Util import FileWriter
import urllib2

"""
GCMD Parameter
"""

class Parameter:
   def __init__(self):
       self.levels=[]
   def getCat(self):
       return self.cat
   def getTopic(self):
       return self.topic
   def getTerm(self):
       return self.term
   def getLevels(self):
       return self.levels
   def addLevel(self,level):
       self.levels.append(level)
   def setCat(self,cat):
       self.cat=cat
   def setTopic(self,topic):
       self.topic=topic
   def setTerm(self,term):
       self.term=term

   def getLevelsDelimited(self,d):
       levels=""
       for l in self.getLevels():
           levels += l + d
       return levels.strip()[:len(levels)-1]

   def as_sql(self):


       level_1=""
       level_2=""
       level_3=""

       level_count=len(self.getLevels())
       if(level_count==3):
           level_1=self.getLevels()[0]
           level_2=self.getLevels()[1]
           level_3=self.getLevels()[2]

       if(level_count==2):
           level_1=self.getLevels()[0]
           level_2=self.getLevels()[1]

       if(level_count==1):
           level_1=self.getLevels()[0]



       levels=":"
       for level in self.getLevels():
           levels += level + ":"
       levels=levels.strip()[:len(levels)-1]

       sql="INSERT INTO datacaster_parameter (category,topic,term,var_level_1,var_level_2,var_level_3,levels,json) VALUES ('" +self.getCat()+"','" + self.getTopic() + "','" + self.getTerm() + "','"+level_1+"','"+level_2+"','"+level_3+"','" + levels + "','" + self.as_json() + "');"


       return sql

   def as_json(self):
       levels=""

       if(len(self.getLevels())>0):
           for level in self.getLevels():
               levels += '"' + level + '",'
           levels=levels.strip()[:len(levels)-1]
           levels= '"levels":[' + levels + ']'

           json='{"category":"' + self.getCat() + '","topic":"' + self.getTopic() + '","term":"' + self.getTerm() + '",'+levels + '}'
       else:
           json='{"category":"' + self.getCat() + '","topic":"' + self.getTopic() + '","term":"' + self.getTerm() + '"}'

       return json

   def __str__(self):

       levels=""
       for level in self.getLevels():
           levels += level + ":"
       levels=levels.strip()[:len(levels)-1]
       if(levels!=""):
           levels="(" + levels +")"
       return self.getCat() + " " + self.getTopic() + " " + self.getTerm() + " "  + levels


def fetchDataFromURL():
       url="http://gcmd.nasa.gov/OpenAPI/get_valids.py?type=parametersvalid&format=plain_text"
       usock = urllib2.urlopen(url)
       data = usock.read()
       usock.close()
       return data

class Parameters:

   #Initialize with empty parameters list
   def __init__(self):
       self.parameters=[]

   def createSQLFile(self,params,file_name):
        writer=FileWriter(file_name)
        writer.writeLine("BEGIN;");
        writer.writeLine(("DELETE FROM datacaster_parameter;"));
        for p in params:
            writer.writeLine(p.as_sql())
        writer.writeLine("COMMIT;")
        return writer.get_file()

   def createJSONFile(self,params,file_name):
        writer=FileWriter(file_name)
        writer.writeLine("{")
        writer.writeLine('"parameters":[')
        for p in params:
            writer.writeLine(p.as_json() + ",")
        writer.writeLine("]")
        writer.writeLine("}")
        return writer.get_file()
    
        


   #Load GCMD Parametrs from NASA
   def loadParams(self):

       net_tools=NETWORKTools()
       data=net_tools.fetchDataFromURL("http://gcmd.nasa.gov/OpenAPI/get_valids.py?type=parametersvalid&format=plain_text")
       
       #data = fetchDataFromURL()

       lines=data.split("\r\n")
       counter=1
       for line in lines:
           if not line.strip():
               continue
           else:


               row=line.split(" > ")
               size=len(row)

               param=Parameter()

               #print str(size) + " " + row[0] + " " + row[1] + " " + row[2]
               param.setCat(row[0])
               param.setTopic(row[1])
               param.setTerm(row[2])

               if(size>3):
                   for i in range(3,size):
                       param.addLevel(row[i])
                       #print "    " + row[i]

               self.parameters.append(param)

   def getParams(self):
       return self.parameters

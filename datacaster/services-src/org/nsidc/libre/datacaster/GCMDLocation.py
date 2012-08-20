"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""

import urllib2

"""
GCMD Location
"""
class Location:

   def __init__(self):
       self.subregions=[]
   def getCat(self):
       return self.category
   def getType(self):
       return self.type
   def getSubs(self):
       return self.subregions
   def add_sub_region(self,sub_region):
       self.subregions.append(sub_region)
   def set_category(self,category):
       self.category=category
   def set_type(self,type):
       self.type=type
   def as_text(self):
       return self.__str__()
   def __str__(self):
       subs=""
       for sub in self.subregions:
           subs+="(" + sub + ")"
       return self.category + ":" + self.type + " " + subs

#Collection of GCMD Locations
class Locations:
   def __init__(self):
       self.locations=[]
       url="http://gcmd.nasa.gov/OpenAPI/get_valids.py?type=locationvalid&format=plain_text"
       usock = urllib2.urlopen(url)
       data = usock.read()
       usock.close()

       lines=data.split("\r\n")
       counter=1
       for line in lines:
           if not line.strip():
               continue
           else:
               loc=Location()

               row=line.split(" > ")
               size=len(row)

               loc.set_category(row[0])
               loc.set_type(row[1])

               if(size>2):
                   for i in range(2,size):
                       loc.add_sub_region(row[i])

               self.locations.append(loc)
               counter +=1

   def get_locations(self):
       return self.locations

   def print_locations(self):
       for l in self.locations:
           print l

   

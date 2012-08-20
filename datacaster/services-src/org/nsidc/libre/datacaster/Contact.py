"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.datacaster) contains
classes related to the Libre-Datacasting project.
----------------------
"""


"""
This class models a Contact Person.
This person is currently incomplete.
"""
class Contact:

    def __init__(self):
        pass

    def setFirstName(self,firstName):
        self.firstName=firstName

    def setLastName(self,lastName):
        self.lastName=lastName

    def setType(self,type):
        self.type=type

    def setInstitute(self,institute):
        self.institute=institute

    def asJSON(self):
    
        json="{"

        keys=self.__dict__.keys()

        for e in keys:
            json+='"' +e + '":"' + self.__dict__[e] + '",'



        json+="}"

        json=json.replace(",}", "}")
        

        return json

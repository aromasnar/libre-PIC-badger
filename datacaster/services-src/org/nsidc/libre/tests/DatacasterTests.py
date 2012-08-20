"""
author: Geoff Anderson

----------------------
This package (org.nsidc.libre.tests) contains tests
related to the Libre-Datacasting project.
----------------------
"""

"""

These tests relate to the server-side (probably Django...) 
 components of the Datacaster.   

"""

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

import os

import unittest

class  New_TestCase(unittest.TestCase):
    def setUp(self):
        #Initialize a DataCastFactory
        self.castFactory=DataCastFactory()
        #Base directory for writing files
        self.temp_dir=os.getcwdu() + "/test_files/temp_files/"
        self.base_dir=os.getcwd()
        
    """
    Load a datacast from an xml file.
    """
    def test_cast_from_xml_one(self):
        print "TEST-----------"
        cast=self.castFactory.castFromXML(self.base_dir + "/test_files/data_cast_test_file_1.xml")
        #cast=self.castFactory.castFromXML("/home/anderson/Download/AAA.xml")
        print cast.asJSON()
        self.assertTrue(cast.getRid()=="test_1", "Test if cast id (rid) is correct.")

    """
    Load another datacast from an xml file.
    """
    def test_cast_from_xml(self):
        print "-----Load Data-Cast from XML file."
        cast=self.castFactory.castFromXML(self.base_dir + "/test_files/data_cast_test_file_2.xml")
        print cast.asJSON()
        self.assertTrue(cast.getRid()=="A-TEST-1", "Test if cast id (rid) is correct")

    """
    Read data from a url.
    """
    def test_get_data_from_url(self):
        print "-----Fetch data from URL."
        value=NETWORKTools().fetchDataFromURL("http://3rdflatiron.com/test_xml.xml")
        self.assertTrue(value=="<test>A</test>", "Assert that returned value = <test>A</test>")

    """
    Read data from a url and write it to a local file.
    """
    def test_get_data_from_url_and_write_to_file(self):
        print "-----Fetch data from URL and write to local file."
        file_name=NETWORKTools().fetchDataFromURL2File("http://3rdflatiron.com/test_xml.xml", self.temp_dir + "test_file_1.xml")
        expected_value="<test>A</test>"
        value=open(file_name,"r").readline().strip()
        self.assertTrue(value==expected_value, value + "!="+ expected_value  + " File contains unexpected value.")
       
    """
    Initialize a datacast from an xml file located on remote url.
    """ 
    def test_cast_from_xml_via_url(self):
        print "-----Load Data-Cast from URL."
        file=NETWORKTools().fetchDataFromURL2File("http://3rdflatiron.com/cast_jess-test.xml", "/home/anderson/tmp/test_1.xml")
        cast=self.castFactory.castFromXML(file)
        #print cast.asJSON()
        self.assertTrue(cast.getRid()=="3DG","Cast data not correct.")

    """
    Load GCMD Parameters from the NASA.
     You need to set the expected parameter count...
    """
    def test_fetch_GCMD_parameters(self):
        print "-----Fetch GCMD Paratmeters."
        params=Parameters()
        params.loadParams()
        file=params.createSQLFile(params.getParams(), self.temp_dir + "gcmd_params_postgres.sql")
        json_file=params.createJSONFile(params.getParams(), self.temp_dir + "gcmd_params_json.js")
        #Expected number of GCMD Paraters.  Could change...
        param_count=1558
        self.assertTrue(param_count==len(params.getParams()), "Parameter counts don't match.")
       
    """
    Load GCMD Locations from NASA.
        Confirm the current location count...
    """ 
    def test_fetch_GCMD_locations(self):
        print "-----Fetch GCMD Locations"
        locs=Locations()
        location_count=456
        self.assertTrue(location_count==len(locs.get_locations()),"Unexpected number of locations.")
       
    """
    Load GCMD from NASA and load into a database.
    """ 
"""
    def test_load_gcmd_params(self):

            print "-----Pull GCMD Paremters from NASSA and load into database."

            db_conn=DBQuery("dbname=libre_dev user=anderson")

            params=Parameters()
            params.loadParams()
            params_=params.getParams()
            loader = GCMD_Param_Loader("dbname=libre_dev user=anderson")

            result=db_conn.query("SELECT category from datacaster_parameter LIMIT 10")

            rows_before_load=result.rowcount
            

            for p in params_:
                loader.put_param(p)

            loader.__del__()
            
            
            result=db_conn.query("SELECT json from datacaster_parameter LIMIT 10")
            rows_after_load=result.rowcount

            self.assertTrue(rows_before_load==0, "Table should be empty.")
            self.assertTrue(rows_after_load>0, "Table should be loaded.")
            #for row in result:
            #    print row

"""

if __name__ == '__main__':
    unittest.main()

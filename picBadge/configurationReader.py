#Author: Azhar Sikander
#Date: July 17, 2010

import config
from django.conf import settings

## Reading Entries/Text from Text Files (Configuration Files)
class configReader:
    
    configFilesPath = ""
    appConfig = None
    
    def __init__(self, prmConfigFilesPath,prmConfigFileName):
        ### this module overides the "config"'s default opener module.
        def myOpener(name):
            if name[0] != '/':
                name = prmConfigFilesPath + name
            return file(name, 'rb')
        config.streamOpener = myOpener
        self.appConfig = config.Config(prmConfigFileName)
        self.configFilesPath = prmConfigFilesPath        
    
    def getConfigHandler(self):
        return self.appConfig
    
    def setConfigFilesPath(self, prmPath):
        self.configFilesPath = prmPath
        
    def getConfigFilesPath(self):
        return self.configFilesPath
    
    def getChoices(self, prmProperty):        
        return [(k, v) for k, v in prmProperty.choices.iteritems()]  
    
    def getInitial(self, prmProperty):
        return prmProperty.initialChoice 
        
    #### READING AGREEMENT TEXT FROM TEXT FILES ####
    # a file exists if you can open and close it
    def exists(self, prmFileName):
        try:
            f = open(prmFileName)
            f.close()
            return True
        except:
            return False
    
    ## reads agreement text from the file    
    def getAgreement(self, prmFileName):
        filename = self.configFilesPath + prmFileName
        if self.exists(filename):
            try:
                fin = open(filename)
                text = fin.read()                
            except:
                text = "Error Reading Agreement Text from File"
            else:
                fin.close()
            return text
        else:
            return "File %s does not exist!" % filename
   
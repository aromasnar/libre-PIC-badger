# Author:	Azhar Sikander
# This file contains Eror Handling class and all the error messages.
import sys
from xml.dom.minidom import Document
		
# This class generates all the error messaged for the api. (in xml format)
class ErrorHandler:	
	
	pythonErrorMsg = "Some error occured while processing the information provided. Check your answers."
	PICAPIErrorMsg = "Unable to get license from pic licensing web service."	
	DataNotProvidedErrorMsg = "Data not provided in the required fields."
	InvalidInputErrorMsg = "Invalid data is entered in one/more fields."
	
	def PythonError(self, errorMessage=""):		
		return self.generateErrorMessage("pythonerr", self.pythonErrorMsg)
	
	def PICAPIError(self, errorMessage=""):
		return self.generateErrorMessage("picapierr", self.PICAPIErrorMsg)	
	
	def generalError(self, errorMessage=""):
		return self.generateErrorMessage("picbadgeapperr", errorMessage)
	
	def DataNotProvidedError(self):
		return self.generateErrorMessage("picbadgeapperr", self.DataNotProvidedErrorMsg)
	
	def InvalidInputError(self):
		return self.generateErrorMessage("picbadgeapperr", self.InvalidInputErrorMsg)
		
	def generateErrorMessage(self, errorID, errorMessage):
		doc = Document()
		errorNode = doc.createElement("error")		
		
		errorIdNode = doc.createElement("id")
		idTextNode = doc.createTextNode(errorID)
		errorIdNode.appendChild(idTextNode)
		
		errorMessageNode = doc.createElement("message")
		msgTextNode = doc.createTextNode(errorMessage)
		errorMessageNode.appendChild(msgTextNode)
		
		errorNode.appendChild(errorIdNode)
		errorNode.appendChild(errorMessageNode)
		
		doc.appendChild(errorNode)
		
		return doc.toxml()

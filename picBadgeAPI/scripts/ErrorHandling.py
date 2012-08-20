# Author:	Azhar Sikander
# This file contains all error messages and their a handler class.
import sys
from xml.dom.minidom import Document

# This class generates all the error messaged for the api. (in xml format)
class Callable:
	def __init__(self, anyCallable):
		self.__call__ = anyCallable
		
class ErrorHandler:	
	
	pythonError = "Unable to process the data you provided. Check your answers."
	CCServerError = "Unable to generate CC part of the license. please verify that you entered valid data"
	
	def PythonError(self, errorMessage=""):
		return self.generateErrorMessage("picbadgeapierr", self.pythonError)
	
	def CCServerError(self, errorMessage=""):
		return self.generateErrorMessage("ccservererr", self.CCServerError)
	
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

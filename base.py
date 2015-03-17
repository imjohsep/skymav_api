import json
import sys
from flask import request

class Base(object):
	method = ''
	message = ''
	headers = ''

	"""Base is the Parent of all API Request classes"""
	def __init__(self, request):
		self.request = request
		self.setMethod()
		self.setMessage()
		self.setHeaders()
	
	def getMethod(self):
		return self.method

	def setMethod(self):
		if (self.request.method != ''):
			self.method = self.request.method
		else:
			return False 	

	def getMessage(self):
		return self.message

	def setMessage(self):
		if (self.getMethod() == 'POST'):
			try:
				message = self.request.data.decode(encoding='UTF-8') #convertes to string
				self.message = json.loads(message) # creates dictionary
			except Exception as ve:
				print("----ERROR----")
				print(type(ve))
				print(ve)
				print("-------------")
			else:
				return False
		else:
			return False

	def getHeaders(self):
		return self.headers

	def setHeaders(self):
		self.headers = self.request.headers


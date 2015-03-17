import json
import sys
from flask import request

class Waypoint(object):

	def __init__(self, latitude, longitude, altitude):
		self.latitude = latitude
		self.longitude = longitude
		self.altitude = altitude

	def getLatitude(self):
		return self.latitude

	def getLongitude(self):
		return self.longitude

	def getAltitude(self):
		return self.altitude

	def setLatitude(self, latitude):
		self.latitude = latitude

	def setLongitude(self, longitude):
		self.longitude = longitude

	def setAltitude(self, altitude):
		self.altitude = altitude
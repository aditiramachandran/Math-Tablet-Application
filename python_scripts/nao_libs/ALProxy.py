"""
@author Joseph Pinkasfeld
Aldebaran Robotics (c) 2008 All Rights Reserved - This file is confidential.

To use this file soapPy is required

Version : $Id$
"""

import SOAPpy

class MethodMissingMixin(object):
	""" A Mixin' to implement the 'method_missing' Ruby-like protocol. """
	def __getattribute__(self, attr):
		try:
			return object.__getattribute__(self, attr)
		except:
			class MethodMissing(object):
				def __init__(self, wrapped, method):
					self.__wrapped__ = wrapped
					self.__method__ = method
				def __call__(self, *args, **kwargs):
					return self.__wrapped__.method_missing(self.__method__, *args, **kwargs)
			return MethodMissing(self, attr)
		
	def method_missing(self, *args, **kwargs):
		""" This method should be overridden in the derived class. """
		raise NotImplementedError(str(self.__wrapped__) + " 'method_missing' method has not been implemented.")		


class ALProxy(MethodMissingMixin):

	def __init__ (self,ModuleName, ip, port):
		clientSOAP = SOAPpy.SOAPProxy("http://"+ip+":"+port,"urn:albroker")
		self.kikou = clientSOAP.getModuleByName(ModuleName)
		self.moduleBroker = SOAPpy.SOAPProxy("http://" + self.kikou.ip + ":" + self.kikou.port, "urn:albroker")

	def method_missing(self, method, *args, **kwargs):
		return self.moduleBroker.callNaoqi(self.kikou.name,method,args).item


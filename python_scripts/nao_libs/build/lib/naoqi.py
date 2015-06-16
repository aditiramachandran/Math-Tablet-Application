import inaoqi

import motion

def autoBind(myClass):
  """Show documentation for each
  method of the class"""

  # dir(myClass) is a list of the names of
  # everything in class
  myClass.setModuleDescription(myClass.__doc__)

  for thing in dir(myClass):
    # getattr(x, "y") is exactly: x.y
    function = getattr(myClass, thing)
    if callable(function):
      if (function.__doc__):
        if (type(function) == type(myClass.function)):
            if (thing[0] != "_"):  # private method
              myClass.functionName(thing, myClass.getName(), function.__doc__)

              for param in function.func_code.co_varnames:
                if (param != "self"):
                  myClass.addParam(param)

              print "bind ", myClass.getName(), " " , thing, " ", str(len(function.func_code.co_varnames)-1)
              myClass.bindWithParam(myClass.getName(),thing,len(function.func_code.co_varnames)-1)



class ALDocable():
  def __init__(self):
    autoBind(self)

  def function(self):
    pass



class ALBroker(inaoqi.broker):
	def init(self):
		print "init"

class ALModule(inaoqi.module, ALDocable):

  def __init__(self,param):
    inaoqi.module.__init__(self, param)
    ALDocable.__init__(self)

  def methodtest(self):
    print "methodtest"

  def pythonChanged(self, param1, param2, param3):
    print param1
    print param2
    print param3

class ALBehavior(inaoqi.behavior):
	def methodtest(self):
		print "methodtest"

	def log(self, p):
		self.logInBehavior(str(p))

	def pythonChanged(self, param1, param2, param3):
		print param1
		print param2
		print param3



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

class postType(MethodMissingMixin):
	def __init__(self):
		""

	def setProxy(self, proxy):
		self.proxy = proxy

	def method_missing(self, method, *args, **kwargs):
	      list = []
	      list.append(method)
	      for arg in args:
	        list.append(arg)
	      result = 0
	      try:
	            result = self.proxy.pythonPCall(list)
	      except RuntimeError,e:
	            raise e

	      return result



class ALProxy(inaoqi.proxy,MethodMissingMixin):

	def __init__(self, *args):
		self.post = postType()
		self.post.setProxy(self)
		if (len (args) == 1):
			inaoqi.proxy.__init__(self, args[0])
		elif (len (args) == 2):
			inaoqi.proxy.__init__(self, args[0],  args[1])
		else:
			inaoqi.proxy.__init__(self, args[0], args[1], args[2])

	def call(self, *args):
		list = []
		for arg in args:
			list.append(arg)

		return self.pythonCall(list)


	def pCall(self, *args):
		list = []
		for arg in args:
			list.append(arg)

		return self.pythonPCall(list)


	def method_missing(self, method, *args, **kwargs):
	      list = []
	      list.append(method)
	      for arg in args:
	        list.append(arg)
	      result = 0
	      try:
	            result = self.pythonCall(list)
	      except RuntimeError,e:
	            raise e
	            #print e.args[0]

	      return result

	@staticmethod
	def initProxies():
		global ALMemory
		global ALMotion
		global ALFrameManager
		global ALLeds
		global ALLogger
		global ALSensors
		#try:
		ALMemory = ALProxy("ALMemory")
		#except:
		#	print "No proxy to ALMemory"
		try:
			ALFrameManager = ALProxy("ALFrameManager")
		except:
			print "No proxy to ALFrameManager"
		try:
			ALMotion = ALProxy("ALMotion")
		except:
			print "No proxy to ALMotion"
		try:
			ALLeds = ALProxy("ALLeds")
		except:
			print "No proxy to ALLeds"
		try:
			ALLogger = ALProxy("ALLogger")
		except:
			print "No proxy to ALLogger"
		try:
			ALSensors = ALProxy("ALSensors")
		except:
			print "No proxy to ALSensors"


def createModule(name):
	global moduleList
	str = "moduleList.append("+ "module(\"" + name + "\"))"
	print str
	exec ("var=5")
	exec(str)


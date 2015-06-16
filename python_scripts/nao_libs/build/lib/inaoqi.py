# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.36
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _inaoqi
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


setInstance = _inaoqi.setInstance
convertObject = _inaoqi.convertObject
class broker(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, broker, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, broker, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_broker(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _inaoqi.delete_broker
    __del__ = lambda self : None;
    def shutdown(*args): return _inaoqi.broker_shutdown(*args)
    def getGlobalModuleList(*args): return _inaoqi.broker_getGlobalModuleList(*args)
broker_swigregister = _inaoqi.broker_swigregister
broker_swigregister(broker)

class baseModule(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, baseModule, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, baseModule, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_baseModule(*args)
        try: self.this.append(this)
        except: self.this = this
    def BIND_PYTHON(*args): return _inaoqi.baseModule_BIND_PYTHON(*args)
    def bindWithParam(*args): return _inaoqi.baseModule_bindWithParam(*args)
    def exit(*args): return _inaoqi.baseModule_exit(*args)
    def getName(*args): return _inaoqi.baseModule_getName(*args)
    def getBrokerName(*args): return _inaoqi.baseModule_getBrokerName(*args)
    def dataChanged(*args): return _inaoqi.baseModule_dataChanged(*args)
    def setModuleDescription(*args): return _inaoqi.baseModule_setModuleDescription(*args)
    def addParam(*args): return _inaoqi.baseModule_addParam(*args)
    def functionName(*args): return _inaoqi.baseModule_functionName(*args)
    def methodMissing(*args): return _inaoqi.baseModule_methodMissing(*args)
    def version(*args): return _inaoqi.baseModule_version(*args)
    def innerTest(*args): return _inaoqi.baseModule_innerTest(*args)
    __swig_destroy__ = _inaoqi.delete_baseModule
    __del__ = lambda self : None;
baseModule_swigregister = _inaoqi.baseModule_swigregister
baseModule_swigregister(baseModule)

class ALPythonModule(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ALPythonModule, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ALPythonModule, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_ALPythonModule(*args)
        try: self.this.append(this)
        except: self.this = this
    def version(*args): return _inaoqi.ALPythonModule_version(*args)
    def execute(*args): return _inaoqi.ALPythonModule_execute(*args)
    def innerTest(*args): return _inaoqi.ALPythonModule_innerTest(*args)
    __swig_getmethods__["executePython"] = lambda x: _inaoqi.ALPythonModule_executePython
    if _newclass:executePython = staticmethod(_inaoqi.ALPythonModule_executePython)
    __swig_destroy__ = _inaoqi.delete_ALPythonModule
    __del__ = lambda self : None;
ALPythonModule_swigregister = _inaoqi.ALPythonModule_swigregister
ALPythonModule_swigregister(ALPythonModule)
ALPythonModule_executePython = _inaoqi.ALPythonModule_executePython

class ALPythonBehavior(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ALPythonBehavior, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ALPythonBehavior, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_ALPythonBehavior(*args)
        try: self.this.append(this)
        except: self.this = this
    def execute(*args): return _inaoqi.ALPythonBehavior_execute(*args)
    __swig_destroy__ = _inaoqi.delete_ALPythonBehavior
    __del__ = lambda self : None;
ALPythonBehavior_swigregister = _inaoqi.ALPythonBehavior_swigregister
ALPythonBehavior_swigregister(ALPythonBehavior)

class module(baseModule):
    __swig_setmethods__ = {}
    for _s in [baseModule]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, module, name, value)
    __swig_getmethods__ = {}
    for _s in [baseModule]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, module, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_module(*args)
        try: self.this.append(this)
        except: self.this = this
    def BIND_PYTHON(*args): return _inaoqi.module_BIND_PYTHON(*args)
    def exit(*args): return _inaoqi.module_exit(*args)
    def getName(*args): return _inaoqi.module_getName(*args)
    def getBrokerName(*args): return _inaoqi.module_getBrokerName(*args)
    def dataChanged(*args): return _inaoqi.module_dataChanged(*args)
    def methodMissing(*args): return _inaoqi.module_methodMissing(*args)
    def version(*args): return _inaoqi.module_version(*args)
    def innerTest(*args): return _inaoqi.module_innerTest(*args)
    __swig_destroy__ = _inaoqi.delete_module
    __del__ = lambda self : None;
module_swigregister = _inaoqi.module_swigregister
module_swigregister(module)

class behavior(baseModule):
    __swig_setmethods__ = {}
    for _s in [baseModule]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, behavior, name, value)
    __swig_getmethods__ = {}
    for _s in [baseModule]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, behavior, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_behavior(*args)
        try: self.this.append(this)
        except: self.this = this
    def setParentFromName(*args): return _inaoqi.behavior_setParentFromName(*args)
    def setEnabled(*args): return _inaoqi.behavior_setEnabled(*args)
    def isEnabled(*args): return _inaoqi.behavior_isEnabled(*args)
    def addInput(*args): return _inaoqi.behavior_addInput(*args)
    def addOutput(*args): return _inaoqi.behavior_addOutput(*args)
    def addParameter(*args): return _inaoqi.behavior_addParameter(*args)
    def getParameter(*args): return _inaoqi.behavior_getParameter(*args)
    def setParameter(*args): return _inaoqi.behavior_setParameter(*args)
    def addOutputLink(*args): return _inaoqi.behavior_addOutputLink(*args)
    def addParameterLink(*args): return _inaoqi.behavior_addParameterLink(*args)
    def addLink(*args): return _inaoqi.behavior_addLink(*args)
    def BIND_PYTHON(*args): return _inaoqi.behavior_BIND_PYTHON(*args)
    def setModuleDescription(*args): return _inaoqi.behavior_setModuleDescription(*args)
    def addParam(*args): return _inaoqi.behavior_addParam(*args)
    def exit(*args): return _inaoqi.behavior_exit(*args)
    def getName(*args): return _inaoqi.behavior_getName(*args)
    def getBrokerName(*args): return _inaoqi.behavior_getBrokerName(*args)
    def dataChanged(*args): return _inaoqi.behavior_dataChanged(*args)
    def methodMissing(*args): return _inaoqi.behavior_methodMissing(*args)
    def version(*args): return _inaoqi.behavior_version(*args)
    def innerTest(*args): return _inaoqi.behavior_innerTest(*args)
    def logInBehavior(*args): return _inaoqi.behavior_logInBehavior(*args)
    __swig_destroy__ = _inaoqi.delete_behavior
    __del__ = lambda self : None;
behavior_swigregister = _inaoqi.behavior_swigregister
behavior_swigregister(behavior)

class proxy(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, proxy, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, proxy, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _inaoqi.new_proxy(*args)
        try: self.this.append(this)
        except: self.this = this
    def pythonCall(*args): return _inaoqi.proxy_pythonCall(*args)
    def pythonPCall(*args): return _inaoqi.proxy_pythonPCall(*args)
    __swig_destroy__ = _inaoqi.delete_proxy
    __del__ = lambda self : None;
proxy_swigregister = _inaoqi.proxy_swigregister
proxy_swigregister(proxy)

ALNAMESIZE = _inaoqi.ALNAMESIZE
class ALSharedClass(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, ALSharedClass, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, ALSharedClass, name)
    __repr__ = _swig_repr
    __swig_setmethods__["m_name"] = _inaoqi.ALSharedClass_m_name_set
    __swig_getmethods__["m_name"] = _inaoqi.ALSharedClass_m_name_get
    if _newclass:m_name = _swig_property(_inaoqi.ALSharedClass_m_name_get, _inaoqi.ALSharedClass_m_name_set)
    def getName(*args): return _inaoqi.ALSharedClass_getName(*args)
    def setName(*args): return _inaoqi.ALSharedClass_setName(*args)
    def serialize(*args): return _inaoqi.ALSharedClass_serialize(*args)
    def __eq__(*args): return _inaoqi.ALSharedClass___eq__(*args)
    def toString(*args): return _inaoqi.ALSharedClass_toString(*args)
    def ALSerialize(*args): return _inaoqi.ALSharedClass_ALSerialize(*args)
    def __init__(self, *args): 
        this = _inaoqi.new_ALSharedClass(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _inaoqi.delete_ALSharedClass
    __del__ = lambda self : None;
ALSharedClass_swigregister = _inaoqi.ALSharedClass_swigregister
ALSharedClass_swigregister(ALSharedClass)

class dummySharedClass(ALSharedClass):
    __swig_setmethods__ = {}
    for _s in [ALSharedClass]: __swig_setmethods__.update(getattr(_s,'__swig_setmethods__',{}))
    __setattr__ = lambda self, name, value: _swig_setattr(self, dummySharedClass, name, value)
    __swig_getmethods__ = {}
    for _s in [ALSharedClass]: __swig_getmethods__.update(getattr(_s,'__swig_getmethods__',{}))
    __getattr__ = lambda self, name: _swig_getattr(self, dummySharedClass, name)
    __repr__ = _swig_repr
    __swig_setmethods__["param1"] = _inaoqi.dummySharedClass_param1_set
    __swig_getmethods__["param1"] = _inaoqi.dummySharedClass_param1_get
    if _newclass:param1 = _swig_property(_inaoqi.dummySharedClass_param1_get, _inaoqi.dummySharedClass_param1_set)
    __swig_setmethods__["param2"] = _inaoqi.dummySharedClass_param2_set
    __swig_getmethods__["param2"] = _inaoqi.dummySharedClass_param2_get
    if _newclass:param2 = _swig_property(_inaoqi.dummySharedClass_param2_get, _inaoqi.dummySharedClass_param2_set)
    def setParam1(*args): return _inaoqi.dummySharedClass_setParam1(*args)
    def getName(*args): return _inaoqi.dummySharedClass_getName(*args)
    def __init__(self, *args): 
        this = _inaoqi.new_dummySharedClass(*args)
        try: self.this.append(this)
        except: self.this = this
    def serialize(*args): return _inaoqi.dummySharedClass_serialize(*args)
    def toString(*args): return _inaoqi.dummySharedClass_toString(*args)
    def ALSerialize(*args): return _inaoqi.dummySharedClass_ALSerialize(*args)
    __swig_destroy__ = _inaoqi.delete_dummySharedClass
    __del__ = lambda self : None;
dummySharedClass_swigregister = _inaoqi.dummySharedClass_swigregister
dummySharedClass_swigregister(dummySharedClass)




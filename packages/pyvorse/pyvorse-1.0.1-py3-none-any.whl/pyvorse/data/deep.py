__all__ = ["deep", "dci", "DeepClass"]

from pyvorse.core import copyAllProps

class deep(dict):
    """Like dict, allows to use prototype hierarchy, and access entries as attribute for get-obly mode. use methodes, with names starts with 'deep'"""
    def __init__(self, *args, **kwargs):
        super(deep, self).__init__(*args, **kwargs)
        self.proto = None # Property, thzat saves link to prototype object
        self.deepinstance = None # used only if object is instance of deep class
    
    def deepget(self, name, *, depth:int = 0):
        if name in self:
            return self[name]
        elif self.proto == None:
            raise KeyError(f"No key '{name}' in object. Depth = {depth}")
        else:
            return self.proto.deepget(name, depth= depth + 1)
    
    def deephas(self, name):
        if name in self:
            return True
        elif self.proto == None:
            return False
        else:
            return self.proto.deephas(name)
    
    def deepfind(self, name):
        "Returns instance in hirerarchy, that has a key, passed as argument. Returns None if nothing found."
        if name in self:
            return self
        elif self.proto == None:
            return None
        else:
            return self.proto.deepfind(name)
    
    def deepset(self, name, value):
        "Allows to set value on key with actual key depth, or on depth 0 if key not found"
        if self.deephas(name):
            self.deepfind[name] = value
            return self
        self[name] = value
    
    def deepdel(self, name):
        "Allows to delete entry on key with actual key depth, or on depth 0 if key not found"
        if self.deephas(name):
            del self.deepfind(name)[name]
            return self
    
    def setproto(self, proto):
        self.proto = proto
        return self
    
    def fill(self, **kwargs):
        for key, value in kwargs.items():
            self.deepset(key, value)
        return self
    
    def up(self):
        return self.proto
    
    def upsafe(self):
        return self.proto if self.proto != None else self
    
    def hasprototype(self):
        return False if self.proto == None else True
    
    def isdeepinstance(self):
        "Tests object to be an instance of some deep class, use .deepinstance to get deepclass object"
        return self.deepinstance != None
    
    def __getattr__(self, name):
        return self.deepget(name)
    
    @classmethod
    def create(cls, proto=None, *origins, **kwargs):
        if not isinstance(proto, deep):
            raise TypeError("Only deep object can be uset as prototype for other deep objects.")
        return cls(*origins).setproto(proto).fill(*kwargs)
    
    def callAsMethod(self, name, *args, **kwargs):
        "Allows calling functions inside deep object, passing deep object as first argument"
        o = self.deepget(name)
        if not callable(o):
            raise TypeError("object exists, but not callable")
        return o(self, *args, **kwargs)
    
    def copy(self):
        "Creates full copy of object"
        o = self.__class__(super(deep, self).copy()) # not an error, super of deep, to prevent erros on cloning deepclasses
        copyAllProps(o, self)
        return o




"""
LEXICON:
prototype - only in classes. Link to object, that will be used as prototype for instancesself.
proto - inside any deep object, link to the prototype of object itself.
"""

class deepclass(deep):
    """Builder for any deep objects with prototype, created deep object wit prototype from deepclass.
    You can extend the deepclass by method .extend(new_prototype). Works like class for"""
    def __init__(self, prototype = None):
        super(deepclass, self).__init__()
        self.prototype = prototype # contains link to proto object for created objects
        self.ensure = None
    
    def setprototype(self, prototype: deep):
        "set deep object, that be set as proto of instances for it."
        self.prototype = prototype
        return self
    
    def setparent(self, parent):
        self.parent = parent
        return self
    
    def ensurefields(self, *names:str):
        self.ensure = tuple(names)
        return self
    
    def extend(self, new_prototype: deep, *names: str):
        dc = deepclass.create(self).setparent(self).setprototype(new_prototype).ensurefields(*names)
        return dc._chainfix()
    
    def _chainfix(self):
        if not self.prototype.proto is self.proto.prototype:
            self.prototype.setproto(self.proto.prototype)
        return self
    
    def new(self, **kwargs):
        o = self.prototype.__class__.create(self.prototype, **kwargs)
        o.deepinstance = self
        for name in self.ensure:
            o[name] = None
        return o


dci = deepclass()

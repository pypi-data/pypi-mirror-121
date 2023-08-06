__all__ = ['attribute', 'w', 'basis', 'throws', 'isthrows',
           'trycall', 'Operators', 'calloperators', 'functor', 'reprint', "safe", "copyAllProps"]

from typing import Callable
from enum import IntFlag, auto
from functools import wraps
########################################################################

# Allows converting function to an object, that
class attribute:
    "Processor, that allows to call function with name, passed as access to attribute of an object."

    def __init__(self, func):
        if callable(func):
            self.__function__ = func
        else:
            raise ValueError("Object is not callable")

    def __call__(self, name):
        return self.__function__(name)

    def __getattr__(self, name):
        return self.__function__(name)

    def __getitem__(self, name):
        return self.__function__(name)


# w.some_word == "some_word"
@attribute
def w(name: str):
    "Other way to in-code write identifier strings"
    return name

########################################################################

# base class with some modifications
class basis(object):
    "Alternative base class. Rewrite representation with .repr(self, data=None) method"

    def __str__(self, data=None):
        return self.repr(data)

    def repr(self, data=None):
        if data != None:
            return f"[{self.__class__.__qualname__}]: {data}"
        return f"[{self.__class__.__qualname__}]"

    def __repr__(self, data=None):
        return self.repr(data)

    @classmethod
    def new(cls, *args, **kwargs):
        return cls(**kwargs)

    @classmethod
    def getClass(cls):
        return cls

    @classmethod
    def getClassName(cls):
        return cls.__name__

    @classmethod
    def getClassQualName(cls):
        return cls.__qualname__

    def id(self):
        return id(self)

    def hexid(self):
        return hex(id(self))

    def __hash__(self):
        return id(self)

    def getAttribute(self, name: str, default = None):
        "Safely access attribute"
        return getattr(self, name, default)


########################################################################
# Marks function with possible exception classes, us ass callable decorator
def throws(*exceptions):
    """Marks method with exceptions, that can throw
    Callable decorator:
    
    @throws(ValueError, IndexError)
    def function():
        pass
    """
    def editor(func: Callable):
        func.__throws__ = tuple(exceptions)
        return func
    return editor

# For testing before invoking
def isthrows(func: Callable, cls):
    """Tests function to __throws__ property"""
    if not hasattr(func, '__throws__'):
        return False
    return cls in func.__throws__

# alternative for using try: except:
def trycall(func: Callable, *args, **kwargs):
    """Calls function inside try:except:
    use like:
    result, exception = trycall(getattr, o, "attrname")
    """
    try:
        return (func(*args, **kwargs), None)
    except BaseException as e:
        return (None, e)

# Safe wrapper for fuction
def safe(func: Callable):
    """Converts function to version, thst called safely, not throws exceptions.
    Returns tuple with 2 elments:
    - if no error: (result, None)
    - if error: (None, exception_object)
    converted functions can be used as:
    result, exception = safefunc()
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return trycall(func, *args, **kwargs)
    return wrapper

###########################################################################
# Wrapper for calling function on operators

class Operators(IntFlag):
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    Divide = auto()
    FloorDivide = auto()
    Modulo = auto()
    Power = auto()
    All = Add | Subtract | Multiply | Divide | FloorDivide | Modulo | Power

class OperandHandler(basis):
    def __init__(self, func: Callable, op: Operators):
        self.__operators__ = {}
        self.__oncall__ = func
        self.append(func, op)

    def append(self, func: Callable, op: Operators):
        self.__operators__[op] = func
        return self

    def __add__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Add in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Add.name} not supported")

    def __sub__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Subtract in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Subtract.name} not supported")

    def __mul__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Multiply in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Multiply.name} not supported")

    def __floordiv__(self, other):
        for key, value in self.__operators__.items():
            if Operators.FloorDivide in key:
                return value(other)
        raise ValueError(
            f"Operator {Operators.FloorDivide.name} not supported")

    def __truediv__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Divide in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Divide.name} not supported")

    def __mod__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Modulo in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Modulo.name} not supported")

    def __pow__(self, other):
        for key, value in self.__operators__.items():
            if Operators.Power in key:
                return value(other)
        raise ValueError(f"Operator {Operators.Power.name} not supported")

    def __call__(self, *args, **kwargs):
        return self.__oncall__(*args, **kwargs)

    def editoperands(self, op: Operators):
        def wrapper(func: Callable):
            self.append(func, op)
        return wrapper

def calloperators(op: Operators = Operators.All):
    """Callable decorator, allows function to be called on using it as operand of some operator.exe
    Using:
    @calloperators(Operators.All)
    def reprint(*args, **kwargs):
        print(*args, **kwargs)
        if len(args) == 1:
            return args[0]
    """
    def wrapper(func: Callable):
        return OperandHandler(func, op)
    return wrapper

@calloperators(Operators.All)
def reprint(*args, **kwargs):
    print(*args, **kwargs)
    if len(args) == 1:
        return args[0]

##########################################################################
# Functor wrapper

def functor(func: Callable):
    """Converts function to it`s copy, that will be called with function object as first argument.
    ```py
    @functor
    def bug(functor, arg*):
        # you can use properties of function
        return functor.__name__
    ```
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(wrapper, *args, **kwargs)
    return wrapper

##########################################################################
class unibox(basis):
    """Container for data. Item accessors uses metadata dictionary. Allows stopping.
    On iteratio - key-value pairs of metadata. Attribute get-access - derivied to item inside container.
    Data can be fully accessed by «.inbox» field.
    """

    def __init__(self, o=None, meta={}):
        self.inbox = o.inbox if isinstance(o, self.getClass()) else o
        self.meta = meta
        self.stopped: bool = False

    def __getitem__(self, name):
        return self.meta[name]

    def __setitem__(self, name, value):
        self.meta[name] = value

    def __delitem__(self, name):
        del self.meta[name]

    def __contains__(self, name):
        return self.meta.__contains__(name)

    def get(self, name, default=None):
        try:
            return self.meta[name]
        except (KeyError, NameError, IndexError, AttributeError):
            return default

    def __getattr__(self, name):
        return getattr(self.inbox, name)

    def clearmeta(self):
        self.meta.clear()

    def setval(self, value):
        self.inbox = value
        return self

    def __iter__(self):
        return self.meta.items()

    def stop(self):
        self.stopped = True
        return self

    def unstop(self):
        self.stopped = False
        return self

    def isStopped(self):
        return self.stopped


##########################################################################
# Dangerous
def copyAllProps(dest, source):
    "Forces object to clone all properties, not started from duble underscore '__'"
    dd = source.__dict__
    for key, value in dd.items():
        if not key.startswith('__'):
            setattr(dest, key, value)

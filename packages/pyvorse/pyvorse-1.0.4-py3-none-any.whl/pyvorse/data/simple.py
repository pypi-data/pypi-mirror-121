__all__ = ["loop", "scope", "stack"]

from pyvorse.core import basis

class loop(list, basis):
    "List, but works with indexes in a different way. Works as looped list. Iterations in cycle ar finite."

    def __getitem__(self, index):
        index = index % len(self)
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        index = index % len(self)
        return super().__setitem__(index, value)

    def __delitem__(self, index):
        index = index % len(self)
        return super().__delitem__(index)

    def insert(self, index, object):
        index = index % len(self)
        return super().insert(index, object)

    def pop(self, index):
        index = index % len(self)
        return super().pop(index)

    def first(self, index: int = 0):
        return self[index]

    def last(self, index: int = 0):
        return self[len(self) - index - 1]
    

class scope(dict, basis):
    "Actualy dict, but extended wit attribute-like access. Iterating by default equivalent to dict.items(). Allows to find value by index «.(index: int)»"

    def __call__(self, index: int):
        return self.getByIndex(index)
    
    def getByIndex(self, index: int):
        return tuple(self.values())[index]
    
    def getKeyByIndex(self, index: int):
        return tuple(self.keys())[index]
    
    def __iter__(self):
        return self.items()
    
    def __getattr__(self, name):
        return self[name]
    
    def __setattr__(self, name, value):
        if name in self:
            self[name] = value
        super().__setattr__(name, value)
    
    def clone(self):
        return scope(super().clone())
    
    def getDynamic(self, key):
        "if value is callable, returns result of calling it function or method, with scope instance as first arg."
        if callable(self[key]):
            return self[key](self)
        return self[key]


class stack(list, basis):
    """Simplest stack realization based on list. Use .push and .pull methods
    You can use validation function, set with .setvalidation(callback(stack, item))
    Full list, but with new methods."""
    validator = None

    def setvalidation(self, callback):
        self.validator = callback
        return self
    
    def validate(self, value) -> bool:
        if callable(self.validator):
            return self.validator(self, value)
        return True

    def push(self, item):
        if self.validate(item):
            return self.append(item)
        raise ValueError(f"Item blocked by validator, use .append to ignore it. // {item}")
    
    def pushes(self, *items):
        for item in items:
            self.push(item)
        return self
    
    def pull(self):
        return self.pop()
    
    def leftpush(self, item):
        if self.validate(item):
            return self.insert(0, item)
        raise ValueError(
            f"Item blocked by validator, use .append to ignore it. // {item}")

    def leftpushes(self, *items):
        for item in items:
            self.leftpush(item)
        return self

    def leftpull(self):
        return self.pop(0)
    
    def repr(self, data=None):
        return " >> ".join(map(str, self))
    
    def empty(self) -> bool:
        return len(self) == 0
    

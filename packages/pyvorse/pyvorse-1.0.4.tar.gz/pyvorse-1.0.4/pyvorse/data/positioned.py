__all__ = ["poslist"]

from pyvorse.core import trycall

class poslist(dict):
    """Behaves mostly like default list, but saves positions, allows skipsself. Trigger - value used as «null» for skipping cells"""

    def __init__(self, *values, trigger=None):
        self.next = 0
        if len(values) > 0:
            self.appends(*values, trigger=None)

    def _autoupdate(self):
        self.next = self._getmaxindex() + 1

    def _getmaxindex(self):
        return trycall(max, tuple(self.keys()))[0] or 0
        

    def append(self, value):
        self[self.next] = value
        self._autoupdate()
        return self
    
    def insert(self, value, index: int = None):
        if index == None:
            index = self.next
        self[index] = value
        self._autoupdate()
        return self
    
    def skip(self):
        self.next += 1
    
    def appends(self, *values, trigger=None):
        "Use trigger to mark skip slots."
        for value in values:
            if value == trigger:
                self.skip()
            else:
                self.append(value)
        return self

    
    def __iter__(self):
        for value in self.values():
            yield value
    
    def indexes(self):
        return self.keys();
    
    def getor(self, index, default=None):
        if not index in self:
            return default
        return self[index]
    
    def __setitem__(self, index, value):
        self._autoupdate();
        return super().__setitem__(index, value)
    
    def __delitem__(self, index):
        self._autoupdate()
        return super().__delitem__(index)
    
    def indexes(self):
        return self.keys()
    
    def pop(self, key):
        res = super().pop(key)
        self._autoupdate()
        return res
    
    def popitem(self):
        res = super().popitem()
        self.autoupdate()
        return res

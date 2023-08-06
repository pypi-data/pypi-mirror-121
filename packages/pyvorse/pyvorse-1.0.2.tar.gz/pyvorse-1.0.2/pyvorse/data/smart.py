__all__ = ["smartlist", "handle", "objectAddress"]

from typing import Callable
from pyvorse.core import basis, unibox


class smartlist(list):
    "List, with additional methods like foreach, find..."

    def find(self, finder: Callable):
        "uses function with 3 arguments (value, index, _list)\nreturns tuple (item, index) or (None, None)"
        i = 0
        for item in self:
            if finder(item, i, self):
                return item, i
            i += 1
        return None, None
    
    def select(self, finder: Callable):
        "uses function with 3 arguments (value, index, _list)\nreturns value or None"
        i = 0
        for item in self:
            if finder(item, i, self):
                return item
            i += 1
        return None
    
    def filtered(self, finder: Callable):  # iterator
        "Custom iterator, that generates only values filtered by predicate"
        i = 0
        for item in self:
            if finder(item, i, self):
                yield item
            i += 1
    
    def filter(self, finder: Callable):
        "returns new instance of smart list with filtered values from initial smart list"
        return smartlist([item for item in self.filtered(finder)])
    
    def any(self, predicate: Callable):
        "Returns true if at least one of values returns true on predicate call. Predicate(value, index, _list)"
        i = 0
        for item in self:
            if predicate(item, i, self):
                return True
            i += 1
        return False
    
    def all(self, predicate: Callable):
        "Returns true if at all values returns true on predicate call. Predicate(value, index, _list)"
        i = 0
        for item in self:
            if not predicate(item, i, self):
                return False
            i += 1
        return True
    
    def astuple(self):
        return tuple(self)
    
    def asset(self):
        return set(self)
    
    def aslist(self):
        return list(self)
    
    # works
    def foreach(self, func: Callable):
        "Calls function for every element in list. Func(value, index, _list)"
        i = 0
        for item in self:
            func(item, i, self)
            i += 1
    
    def mapper(self, func: Callable):
        "Calls function for every element in list and writs it return to result list. Func(value, index, _list)"
        i = 0
        result = smartlist()
        for item in self:
            result.append(func(item, i, self))
            i += 1
        return result

    def reducer(self, func: Callable, previnit = None):
        "Reduces list to one result value. Func(prev, value, index, _list)"
        i = 0
        prev = previnit
        for item in self:
            prev = func(prev, item, i, self)
            i += 1
        return prev
    
    def sort(self, sorter: Callable, invert:bool=False):
        """Sorter(value1, value2)
        Returns: -1 >>> value1 < value2
        Returns: 0  >>> value1 == value2
        Returns: 1  >>> value1 > value2
        In result - larger moved to th end of list.
        You can use invert argument all.reverse() method
        """
        self._sort(0, len(self) - 1, sorter=sorter)
        if invert: self.reverse()
        return self
    
    def _partiate(self, start, end, *, sorter):
        pivot = self[start]
        low = start + 1
        high = end

        while True:
            # If the current value we're looking at is larger than the pivot
            # it's in the right place (right side of pivot) and we can move left,
            # to the next element.
            # We also need to make sure we haven't surpassed the low pointer, since that
            # indicates we have already moved all the elements to their correct side of the pivot
            while low <= high and sorter(self[high], pivot) > -1:
                high = high - 1

            # Opposite process of the one above
            while low <= high and sorter(self[low], pivot) < 1:
                low = low + 1

            # We either found a value for both high and low that is out of order
            # or low is higher than high, in which case we exit the loop
            if low <= high:
                self[low], self[high] = self[high], self[low]
                # The loop continues
            else:
                # We exit out of the loop
                break

        self[start], self[high] = self[high], self[start]

        return high

    def _sort(self, start, end, *, sorter):
        if start >= end:
            return

        p = self._partiate(start, end, sorter=sorter)
        self._sort(start, p-1, sorter=sorter)
        self._sort(p+1, end, sorter=sorter)
    
    def sliced(self, start, end):
        return smartlist(self[start:end])
    
    def slicedstart(self, start):
        return smartlist(self[start:])
    
    def slicedend(self, end):
        return smartlist(self[:end])


class handle(basis):
    """Line of handlers for an object"""

    def __init__(self):
        super().__init__()
        self.way = []
    
    def __call__(self, callback):
        "callback uses one argument, link to current values."
        self.way.append(callback)
        return self
    
    def use(self, data):
        if isinstance(data, unibox):
            return self._use(data)
        return self._use(unibox(data))

    def _use(self, box):
        i = -1 # 0 on first iteration
        for cb in self.way:
            i += 1
            box["Step"] = i
            if not box.stopped:
                try:
                    cb(box)
                except Exception as e:
                    if not "errors" in box:
                        box["errors"] = []
                    box["errors"].append(e)
        return box


class objectAddress(basis):
    """Saves linear cobination of keys and indexes, and callbacks for any object. Used for deep structures,
    accessed wit [] operator"""
    def __init__(self):
        super(objectAddress, self).__init__()
        self.way = []
    
    def __call__(self, callback):
        "callback uses one argument, link to current values."
        self.way.append(callback)
        return self
    
    def __getitem__(self, key):
        "callback uses one argument, link to current values."
        self.way.append(key)
        return self
    
    def use(self, o):
        tmp = o
        for key in self.way:
            if callable(key):
                tmp = key(tmp)
            else:
                tmp = tmp[key]
        return tmp

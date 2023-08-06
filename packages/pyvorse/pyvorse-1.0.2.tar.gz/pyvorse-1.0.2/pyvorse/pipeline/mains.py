from typing import Callable
from pyvorse.core import basis
from pyvorse.tests import isinrange

class DictionaryPipeline(dict):
    "Represents package of function, with access by it`s names. In cell uses item ['target'] for select next. "
    def __call__(self, func: Callable):
        if not hasattr(func, "__name__"):
            return func
        self[func.__name__] = func
        return self
    
    def append(self, funcOrName):
        "Advanced append decorator, that allows rename function"
        if callable(funcOrName) and hasattr(funcOrName, "__name__"):
            self[funcOrName.__name__] = funcOrName
            return funcOrName
        elif isinstance(funcOrName, str):
            def decor(func: Callable):
                self[funcOrName] = func
                return func
            return decor
        raise ValueError("Possible used lambda function without name")
    
    def __getattr__(self, name):
        return self[name]
    
    def defaultpointer(self, cell, smeta):
        if not "target" in cell or not cell['target'] in self:
            return
        return self[cell['target']]


class ListPipeline(list):
    "Represents package of function, with access by it`s names. In cell uses item ['target'] for select next. "

    def __call__(self, func: Callable):
        self.apend(func)
        return self

    def append(self, func):
        "Advanced append decorator, that allows rename function"
        self.apend(func)
        return self

    def __getattr__(self, index):
        return self[index]

    def defaultpointer(self, cell, smeta):
        if not "target" in cell or not isinrange(self, cell['target']):
            return
        return self[cell['target']]
    

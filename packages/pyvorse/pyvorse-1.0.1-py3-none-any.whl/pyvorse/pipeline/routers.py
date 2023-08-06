from pyvorse.pipeline.datacell import dcell
from typing import Callable
from pyvorse.core import basis

class router(basis):
    """Class encapsulates functionality of running pipelines.
    """
    def __init__(self, func: Callable = None, meta = {}):
        if not callable(func):
            raise TypeError("Pointer not callable")
        self.pointer = func # can be None
        self.staticmeta = meta
        self.initial = None  # can be None
        self.final = None  # can be None
        self.prestep = None  # can be None
        self.poststep = None  # can be None

    def setup(self, func: Callable):
        self.pointer = func
        return func
    
    def initalizer(self, func: Callable):
        self.initial = func
        return func

    def finalizer(self, func: Callable):
        self.final = func
        return func
    
    def callBeforeStep(self, func: Callable):
        self.prestep = func
        return func
    
    def callAfterStep(self, func: Callable):
        self.poststep = func
        return func

    def launch(self, cell: dcell):
        """Run pipeline with box"""
        if callable(self.initial):
            self.initial(cell, self.staticmeta)
        #=============================
        self._launch(cell)
        #=============================
        if callable(self.final):
            self.final(cell, self.staticmeta)
        return self
    
    def _step(self, cell, selected):
        if callable(self.prestep):
            self.prestep(cell, self.staticmeta)
        #============================
        if not callable(selected):
            return
        selected(cell, self.staticmeta)
        #============================
        handler = self.pointer(cell, self.staticmeta)
        cell["tmp-handler"] = handler
        #============================
        if callable(self.poststep):
            self.poststep(cell, self.staticmeta)
        #============================
        del cell["tmp-handler"] # it`s only temporal metadata for poststep
        return handler
    
    
    def _launch(self, cell):
        if not callable(self.pointer):
            return
        handler = self.pointer(cell, self.staticmeta)
        if cell.stopped:
            return
        #============================
        while not cell.stopped and handler != None:
            handler = self._step(cell, handler)
    
    def __call__(self, cell: dcell):
        return self.launch(cell)
        

__all__ = ["spider"]

from pyvorse.core import basis, unibox
from typing import Callable

class spider(basis):
    """Creates an object with functions that automatically explores complex data structures. 
    Seeker function - to find next element. cb(structure, element, box) -> «next_element». 
    Worker function - to do something with data element.
    Stop box to finish spider walk. """
    def __init__(self, seeker: Callable, worker: Callable):
        self.seeker = seeker
        self.worker = worker
    
    def launch(self, struct):
        dot = struct
        box = unibox()

        while not box.stopped:
            dot = self.seeker(struct, dot, box)
            self.worker(struct, dot, box)
        
        return box
    
    def use(self, struct):
        return self.launch(struct)


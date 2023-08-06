__all__ = ["Selector"]

from pyvorse.core import basis
from typing import Callable, List, Any, Hashable
import random
import json

class Selector(basis):
    """Randomized selections from json-like data"""

    SELECT = random.Random(0)
    @classmethod
    def ResetSeed(cls, x=0):
        cls.SELECT.seed(x)
        return cls.SELECT
    
    
    @classmethod
    def weighted(cls, data: List[List]) -> Any:
        "Data format - List[List[]]. List of lists with len == 2. First value - value, Second - weight of this value. Returns randomly selected value"
        summ = 0
        for pair in data:
            if not isinstance(pair, list): raise TypeError("Object must be a list.")
            if not len(pair) == 2: raise ValueError(f"Pair must have length equal to 2, but is {len(pair)}")
            # Calculate weights sum:
            summ += pair[1]
        
        # Generate value between 0 and $summ, step by step inside variations, and on each step subtract weight. When variable goes 0 or less - select pair, and its value
        var = cls.SELECT.randrange(0, summ)
        # select
        for pair in data:
            var -= pair[1]
            if var <= 0: return pair[0]
        raise Exception("Unknown error with weighted selection")
    
    @classmethod
    def weightedExt(cls, data: List[List]) -> Any:
        "Analog of .weighted, but inner lists can contain more then one value, uses last value as weight. Returns slice of list without last value (weight)"
        summ = 0
        for pair in data:
            if not isinstance(pair, list): raise TypeError("Object must be a list.")
            # Calculate weights sum:
            summ += pair[-1]

        # Generate value between 0 and $summ, step by step inside variations, and on each step subtract weight. When variable goes 0 or less - select pair, and its value
        var = cls.SELECT.randrange(0, summ)
        # select
        for pair in data:
            var -= pair[-1]
            if var <= 0:
                return pair[:-1]
        raise Exception("Unknown error with weighted selection")
    
    @classmethod
    def multi(cls, count: int, method: Callable, *args, **kwargs):
        res = []
        for i in range(count):
            res.append(method(*args, **kwargs))
        return res



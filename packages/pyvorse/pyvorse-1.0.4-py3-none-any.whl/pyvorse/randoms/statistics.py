__all__ = ["Stats"]

from pyvorse.core import basis
from typing import Callable, List, Any, Hashable
import json

class Stats(basis):
    "Methods to obtain statistics for data structures."

    @classmethod
    def statisticsJson(cls, data: List[Any]) -> str:
        "Returns json string with dictionary, with string-represented values as keys, and string with percentage as values."
        res = {}
        count = len(data)
        for v in data:
            key = repr(v)
            if not key in res:
                res[key] = 0
            else:
                res[key] += 1
        for key, value in res.items():
            res[key] = str(round(100 * (value / count), 2)) + '%'
        return json.dumps(res, indent=4, ensure_ascii=False)

    @classmethod
    def statisticsDict(cls, data: List[Hashable]) -> str:
        "Returns json string with dictionary, with string-represented values as keys, and string with percentage as values."
        res = {}
        count = len(data)
        for v in data:
            if not v in res:
                res[v] = 0
            else:
                res[v] += 1
        for key, value in res.items():
            res[key] = str(round(100 * (value / count), 2)) + '%'
        return res

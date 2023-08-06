__all__ = ["hashable", "haskey", "isand", "isor", "eqand", "eqor", "haslen"]

from typing import overload


def hashable(elem):
    """
    Returns True if element is able to hash and vice-versa
    """
    try:
        x = iter(elem)
        next(x)
    except:
        return False
    else:
        return True


def haskey(item, key):
    try:
        item[key]
    except (IndexError, KeyError):
        return False
    else:
        return True


def haslen(item):
    try:
        len(item)
    except (TypeError, AttributeError):
        return False
    else:
        return True


# logic
def isand(elem, *args):
    for x in args:
        if not elem is x:
            return False
    return True


def isor(elem, *args):
    for x in args:
        if elem is x:
            return True
    return False


def eqand(elem, *args):
    for x in args:
        if not elem == x:
            return False
    return True


def eqor(elem, *args):
    for x in args:
        if elem == x:
            return True
    return False

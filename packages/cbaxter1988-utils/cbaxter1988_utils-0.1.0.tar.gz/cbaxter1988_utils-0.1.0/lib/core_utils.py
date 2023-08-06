from copy import deepcopy

from typing import List, Any


def make_tuple(*args):
    return tuple(args)


def len_eq_one(items: List) -> bool:
    if len(items) == 1:
        return True
    else:
        return False


def clone_item(item: Any):
    return deepcopy(item)

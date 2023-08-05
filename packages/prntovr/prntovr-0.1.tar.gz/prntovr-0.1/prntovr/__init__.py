from random import shuffle
from typing import Any
from sys import stdout


def print(*args: Any, end: str = '\r\n') -> Any:
    """
    This function shuffles the args and 'prints' them then (except for 'end' parameter)
    """
    for obj in args:
        if type(obj) == str:
            wns = obj.split()
            shuffle(wns)
            stdout.write(' '.join(wns))
        elif type(obj) == list:
            wns = obj
            shuffle(wns)
            stdout.write(str(wns))
        elif type(obj) == tuple:
            wns = list(obj)
            shuffle(wns)
            stdout.write(str(tuple(wns)))
        elif type(obj) == dict:
            wns = {}
            values = list(obj.values())
            keys = list(obj.keys())
            shuffle(keys)
            shuffle(values)
            for val, key in zip(values, keys):
                wns[key] = val
            stdout.write(str(wns))
        elif type(obj) == int or type(obj) == float:
            wns = list(str(obj))
            shuffle(wns)
            stdout.write(''.join(wns))
        stdout.write(' ')
    stdout.write(end)

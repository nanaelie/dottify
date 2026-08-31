import sys
import functools

from .convert import convert

def wrapped(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        def trace(frame, event, arg):
            if (event == "line" or event == "return") and frame.f_code is func.__code__:
                for k, v in frame.f_locals.items():
                    frame.f_locals[k] = convert(v)
            return trace
            
        sys.settrace(trace)
        try:
            r = func(*args, **kwargs)
        finally:
            sys.settrace(None)
            
        return r
    return wrapper


__all__ = ["wrapped"]
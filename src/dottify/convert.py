from typing import Any
from dottify import Dottify

def convert(obj: Any) -> Any:
    """
    Recursively convert dicts to Dottify.
    Also walks into lists and tuples.
    """
    if isinstance(obj, dict):
        return Dottify({k: convert(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [convert(item) for item in obj]
    if isinstance(obj, tuple):
        return tuple(convert(item) for item in obj)
    return obj


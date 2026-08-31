import sys
from contextlib import contextmanager
from types import FrameType
from typing import Generator

from .core import Dottify

def _convert(value):
    if isinstance(value, Dottify):
        return value

    if isinstance(value, dict):
        return Dottify({
            key: _convert(item)
            for key, item in value.items()
        })

    if isinstance(value, list):
        return [_convert(item) for item in value]

    if isinstance(value, tuple):
        return tuple(_convert(item) for item in value)

    if isinstance(value, set):
        return {_convert(item) for item in value}

    return value


def _convert_locals(frame: FrameType) -> None:
    locals_ = frame.f_locals

    for name, value in list(locals_.items()):
        converted = _convert(value)

        if converted is not value:
            locals_[name] = converted


def _trace(frame: FrameType, event: str, arg):
    if event == "line":
        _convert_locals(frame)

    return _trace


@contextmanager
def dottify_mode() -> Generator[None, None, None]:
    previous_trace = sys.gettrace()

    def trace(frame: FrameType, event: str, arg):
        if event == "line" and frame.f_code is dottify_mode.__code__:
            for k, v in frame.f_locals.items():
                frame.f_locals[k] = _convert(v)

        if event == "call":
            frame.f_trace_lines = True
            return _trace

        return _trace

    sys.settrace(trace)

    try:
        yield
    finally:
        sys.settrace(previous_trace)

from dottify import dottify_mode, Dottify


def test_dottify_mode():
    with dottify_mode():
        data = {"name": "Alice", "address": {"city": "NYC"}}

        assert isinstance(data, Dottify)
        assert isinstance(data.address, Dottify)
        assert data.name == "Alice"

    normal = {"x": 1}

    assert type(normal) is dict


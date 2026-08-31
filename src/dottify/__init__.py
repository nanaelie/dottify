"""
dottify
=======

A lightweight utility that lets you access dictionary keys
as attributes (dot notation), with optional case-insensitive
matching and helpful "did you mean?" error suggestions.

Author: nanaelie
Repository: https://github.com/nanaelie/dottify
License: MIT
"""

from .__version__ import __version__
from .core import Dottify
from .exceptions import DottifyKNFError
from .core import Dottify
from .convert import convert
from .wrapped import wrapped

# Public aliases
dottify = Dottify

__author__ = "nanaelie"
__license__ = "MIT"
__url__ = "https://github.com/nanaelie/dottify"

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "__url__",
    "DottifyKNFError",
    "Dottify",
    "dottify",
    "convert",
    "wrapped",
]

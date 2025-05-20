"""
                        dottify

    A lightweight utility to access dictionary keys
    as attributes (dot notation), with case-insensitive 
    matching and helpful error suggestions.

    Author: nanaelie
    Repository: https://github.com/nanaelie/dottify
    License: MIT
"""

from .dottify import Dottify
from .__version__ import __version__
from .exceptions import *
from .exceptions import __all__ as exceptions

__url__ = "https://github.com/nanaelie/dottify"
__author__ = "nanaelie"
__license__ = "MIT"

__all__ = exceptions + ['Dottify', '__version__', '__url__',
                                '__author__', '__license__']


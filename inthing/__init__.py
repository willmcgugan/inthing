"""
Inthing module
==============


"""
from ._version import VERSION as __version__

from .stream import Stream, Result
from .event import Event

__all__ = ["errors",
           "Result",
           "Stream",
           "Event"]

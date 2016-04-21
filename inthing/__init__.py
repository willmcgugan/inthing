"""
Inthing module
==============


"""
from ._version import VERSION as __version__

from .stream import Stream, AddEventResult
from .event import Event

__all__ = ["Stream", "Event"]

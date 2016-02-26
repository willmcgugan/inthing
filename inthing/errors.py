from __future__ import unicode_literals
from __future__ import print_function


class StreamError(Exception):
    pass


class ConnectivityError(Exception):
    pass


class BadResponse(Exception):
    pass


class EventError(Exception):
    """An error relating to an event"""


class RateLimited(EventError):
    """"Server has imposed a limit"""
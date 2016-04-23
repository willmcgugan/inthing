"""Exceptions raised by inthing module."""

from __future__ import print_function
from __future__ import unicode_literals

import sys


class StreamError(Exception):
    """An error occured when working with a stream."""


class ConnectivityError(StreamError):
    """There was an issue reaching the server."""


class BadResponse(StreamError):
    """The server returned an unexpected response."""


class EventError(StreamError):
    """An error relating to an attempt to post an event."""


class EventFail(EventError):
    """The event contained invalid information."""

    def __init__(self, result):
        self.result = result
        super(EventFail, self).__init__(result.get('msg', 'event failed to validate'))

    def print_error(self):
        result = self.result
        if result.get('status') == 'fail':
            sys.stderr.write(result.get('msg') + '\n')
            for field, errors in result.get('field_errors', {}).items():
                sys.stderr.write(" * {} - {}\n".format(field, ', '.join(errors)))


class RateLimited(EventError):
    """"Events are being posted to fast."""

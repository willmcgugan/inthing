from __future__ import unicode_literals
from __future__ import print_function

import sys

class StreamError(Exception):
    pass


class ConnectivityError(Exception):
    pass


class BadResponse(Exception):
    pass


class EventError(Exception):
    """An error relating to an event"""


class EventCreateError(Exception):
    """An error relating to an event"""

    def __init__(self, result):
        self.result = result
        super(EventCreateError, self).__init__(result.get('msg', 'event failed to validate'))

    def print_error(self):
        result = self.result
        if result.get('status') == 'fail':
            sys.stderr.write(result.get('msg') + '\n')
            for field, errors in result.get('field_errors', {}).items():
                sys.stderr.write(" * {} - {}\n".format(field, ', '.join(errors)))


class RateLimited(EventError):
    """"Server has imposed a limit"""
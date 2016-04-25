"""
Event Class
===========

"""

from __future__ import print_function
from __future__ import unicode_literals


class Event(object):
    """Contains the details of a new event.

    This class provides a more finely grained way of creating events. To use,
     construct an Event instance and add it to a stream with :func:`inthing.Stream.add_event`.

    """

    def __init__(self,
                 title="New Event",
                 type="text",
                 priority=0,
                 markup="markdown",
                 description=None,
                 text=None,
                 generator=None):
        self.title = title
        self.type = type
        self.priority = priority
        self.markup = markup
        self.description = description
        self.text = text
        self.generator = generator

        self.id = None
        self.images = []

    def add_image(self, path):
        """Add an image to the event.

        :param path: Path to an image file
        :type path: str

        """
        self.images.append(path)

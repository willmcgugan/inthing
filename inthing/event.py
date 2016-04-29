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
                 generator=None,
                 code_language=None):
        """Store details for a single event.

        This class is used in the low level interface for creating events. You probably want to
        used the methods on :class:`inthing.Stream` for a simpler interface.

        Here's an example of using this class::

            event = Event(title="Example text event", text="Hello, World!")
            stream.add_event(event)


        :param title: The title of the event, shown as a header.
        :type title: str
        :param type: The type of the event.
        :type type: str
        :param markup: The markup used to render the descriptions, may be 'text', 'html', 'markdown'
        :type markup: str
        :param text: Text associated with the event.
        :type text: str
        :param generator: Text regarding what generated the event.
        :type generator: str
        :param code_language: The language used to syntax highlight code events.
        :type code_language: str

        """
        self.title = title
        self.type = type
        self.priority = priority
        self.markup = markup
        self.description = description
        self.text = text
        self.generator = generator
        self.code_language = code_language

        self.images = []

    def add_image(self, path):
        """Add an image to the event.

        :param path: Path to an image file
        :type path: str

        """
        self.images.append(path)

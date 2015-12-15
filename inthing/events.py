from __future__ import unicode_literals
from __future__ import print_function

import weakref


class EventBase(object):

    def __init__(self):
        self._stream = None
        self.id = None
        super(EventBase, self).__init__()

    @property
    def stream(self):
        return self._stream() if self._stream is not None else None

    def set_stream(self, stream):
        self._stream = weakref.ref(stream)

    def get_event_data(self):
        """Get a dictionary of event information"""
        raise NotImplementedError('events must have a get_event_data method')

    def save(self):
        """Save the event to the stream"""
        if self.stream is not None:
            self.stream._new_event(self)
            return True
        else:
            return False


class Text(EventBase):

    def __init__(self, title, text, markup="markdown"):
        super(Text, self).__init__()
        self.title = title
        self.text = text
        self.markup = markup
        self.save()

    def __repr__(self):
        if self.id is None:
            return "<text>"
        else:
            return "<text {}>".format(self.id)

    def get_event_data(self):
        return {
            "type": "text",
            "title": self.title,
            "text": self.text,
            "markup": self.markup
        }

from __future__ import print_function
from __future__ import unicode_literals


class Event(object):
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
        self.images.append(path)

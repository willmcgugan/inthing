from __future__ import unicode_literals
from __future__ import print_function

import mimetypes
import platform
from os.path import basename
import json

from . import rpc
from . import errors
from . import urls
from .event import Event
from .compat import text_type
from .jsonrpc import JSONRPCError

import requests


class Stream(object):
    """A stream of events"""

    def __init__(self, id=None, password=None, generator=None):
        self.rpc = rpc.get_interface()
        self.id = id
        self.password = password

        if generator is None:
            generator = platform.node()
        self.generator = generator

        self.url = None
        super(Stream, self).__init__()

        if id is not None:
            self._get(id, password)
        else:
            self._new()

    def __repr__(self):
        if self.url is None:
            return "<stream>"
        else:
            return "<stream '{}' {}>".format(self.generator, self.url)

    def _new(self):
        try:
            result = self.rpc.call('stream.new')
        except JSONRPCError as e:
            raise errors.StreamError(text_type(e))
        else:
            self.id = result['id']
            self.url = result['url']
            self.password = result['password']

    def _get(self, stream, password):
        try:
            result = self.rpc.call('stream.get', stream=stream, password=password)
        except JSONRPCError as e:
            raise errors.StreamError(text_type(e))
        self.id = result['id']
        self.url = result['url']
        self.password = password

    def _add_event(self, event):
        """Add an event"""
        post_args = {}
        if event.images:
            path = event.images[0]
            mime_type = mimetypes.guess_type(path)
            files = {
                'image': (basename(path), open(path, 'rb'), mime_type,)
            }
            post_args['files'] = files

        post_args['data'] = {
            'stream': self.id,
            'password': self.password,
            'title': event.title,
            'type': event.type,
            'priority': event.priority,
            'markup': event.markup,
            'text': event.text,
            'generator': event.generator or self.generator
        }

        url = urls.event_url + '?format=json'
        response = requests.post(url, **post_args)

        result = json.loads(response.content)
        print(result)

        return result

    def add_text(self, text, title="Text", markup="markdown"):
        """Add a text event"""
        event = Event(type="text", title=title, text=text, markup=markup)
        self._add_event(event)

    def add_image(self, path, text="", title="New Photo", markup="markdown"):
        """Add an image event"""
        event = Event(type="image", title=title, text=text, markup=markup)
        event.add_image(path)
        self._add_event(event)

    def add(self, event):
        event.set_stream(self)
        event.save()

from __future__ import print_function
from __future__ import unicode_literals

import mimetypes
import platform
import os
import json
import time
import tempfile
import webbrowser
from os.path import basename

from . import errors
from . import urls
from .rpc import get_interface
from .event import Event
from .compat import text_type
from .jsonrpc import JSONRPCError

import requests


class EventResult(object):
    """A succesfully posted event."""

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """Summary with url."""
        return "<event '{}''>".format(self.url)

    def browse(self):
        """Browse to the event."""
        webbrowser.open(self.url)


class Stream(object):
    """A stream of events."""

    def __init__(self, id, password=None, generator=None):
        self.rpc = get_interface()
        self.id = id or os.environ.get('INTHING_STREAM', None)
        self.password = password or os.environ.get('INTHING_STREAM_PASSWORD', None)

        if self.id is None:
            raise ValueError('Stream ID required')

        if generator is None:
            generator = platform.node()
        self.generator = generator

        self.url = None
        super(Stream, self).__init__()

    def __repr__(self):
        """Basic stream info."""
        if self.url is None:
            return "<stream>"
        else:
            return "<stream '{}' {}>".format(self.generator, self.url)

    @classmethod
    def new(cls):
        """Create a new stream."""
        rpc = get_interface()
        try:
            result = rpc.call('stream.new')
        except JSONRPCError as e:
            raise errors.StreamError(text_type(e))
        else:
            stream = cls(id=result['id'],
                         password=result['password'])
            stream.url = result['url']
        return stream

    def browse(self):
        """Open the stream in your browser."""
        webbrowser.open(self.url)

    def _get(self, stream, password):
        try:
            result = self.rpc.call('stream.get', stream=stream, password=password)
        except JSONRPCError as e:
            raise errors.StreamError(text_type(e))
        self.id = result['id']
        self.url = result['url']
        self.password = password

    def _add_event(self, event):
        """Add an event."""
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
            'description':event.description,
            'text': event.text,
            'generator': event.generator or self.generator
        }

        url = urls.event_url + '?format=json'
        try:
            response = requests.post(url, **post_args)
        except requests.ConnectionError as e:
            raise errors.ConnectivityError("unable to contact server")

        try:
            result = json.loads(response.content)
        except Exception as e:
            raise errors.BadResponse('unable to decode response from server ({})'.format(e))

        status = result.get('status', '')

        if status == 'ok':
            return EventResult(result['event']['url'])

        msg = result.get('msg', 'event error')
        if status == 'ratelimited':
            raise errors.RateLimited(msg)

        raise errors.EventCreateError(result)

    def text(self, text, title="Text", markup="markdown"):
        """Add a text event."""
        event = Event(type="text",
                      title=title,
                      description=text,
                      markup=markup)
        result = self._add_event(event)
        return result

    def code(self, code, language=None, description=None, title="Code", markup="markdown"):
        event = Event(type="code",
                      title=title,
                      markup=markup,
                      description=description,
                      text=code)
        result = self._add_event(event)
        return result

    def image(self, path, description=None, title="New Photo", markup="markdown"):
        """Add an image event."""
        event = Event(type="image",
                      title=title,
                      description=description,
                      markup=markup)
        event.add_image(path)
        result = self._add_event(event)
        return result

    def screenshot(self, delay=0, description=None, title="New Screenshot", markup="markdown"):
        if delay:
            time.sleep(delay)
        import pyscreenshot
        filename = tempfile.mktemp(prefix='inthing', suffix=".jpg")
        pyscreenshot.grab_to_file(filename)
        event = Event(type="screenshot", title=title, description=description, markup=markup)
        event.add_image(filename)
        result = self._add_event(event)
        return result

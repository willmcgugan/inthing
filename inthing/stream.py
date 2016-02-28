from __future__ import unicode_literals
from __future__ import print_function

import mimetypes
import platform
import os
import json
import time
import tempfile
from os.path import basename

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
        self.id = id or os.environ.get('INTHING_STREAM', None)
        self.password = password or os.environ.get('INTHING_STREAM_PASSWORD', None)

        if self.id is None:
            raise ValueError('Stream ID required')
        if self.password is None:
            raise ValueError('Password is required')

        if generator is None:
            generator = platform.node()
        self.generator = generator

        self.url = None
        super(Stream, self).__init__()

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
        try:
            response = requests.post(url, **post_args)
        except requests.ConnectionError as e:
            raise errors.ConnectivityError("unable to contact server")

        try:
            result = json.loads(response.content)
        except Exception as e:
            raise errors.BadResponse('unable to decode response from server ({})'.format(e))
    
        status = result.get('status', '')

        if status in ('fail', 'ok'):
            return result

        msg = result.get('msg', 'event error')
        if status == 'ratelimited':
            raise errors.RateLimited(msg)

        raise errors.EventError(msg)

    def text(self, text, title="Text", markup="markdown"):
        """Add a text event"""
        event = Event(type="text", title=title, text=text, markup=markup)
        result = self._add_event(event)
        return result

    def image(self, path, text="", title="New Photo", markup="markdown"):
        """Add an image event"""
        event = Event(type="image", title=title, text=text, markup=markup)
        event.add_image(path)
        result = self._add_event(event)
        return result

    def screenshot(self, delay=0, text="", title="New Screenshot", markup="markdown"):
        if delay:
            time.sleep(delay)
        import pyscreenshot
        filename = tempfile.mktemp(prefix='inthing', suffix=".jpg")
        pyscreenshot.grab_to_file(filename)
        event = Event(type="screenshot", title=title, text=text, markup=markup)
        event.add_image(filename)
        result = self._add_event(event)
        return result


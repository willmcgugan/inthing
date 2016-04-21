"""

Streams
=======


"""

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


class AddEventResult(object):
    """Represents a successfully posted event.

    The ``url`` attribute contains the URL to the the event's page.

    """

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """Summary with url."""
        return "AddEventResult('{}')".format(self.url)

    def browse(self):
        """Browse to the event."""
        webbrowser.open(self.url)


class Stream(object):
    """Inthing Stream class interface.

    This class is the main interface for posting to an Inthing Stream. It represents a single Stream, and has methods to post the various event types.

    """

    def __init__(self, id=None, password=None, generator=None):
        """Construct a new Stream object.

        :param id: The ID of your stream. This may be either a UUID (mixture of letters an numbers),
            or the URL of the stream.
        :type id: str
        :param password: The stream's password, if required. It's possible for a stream to have no
            password, which allows for anyone to post to it.
        :type password: str
        :param generator: A short string to identify what has created this
        :type generator: str
        :rtype: Stream instance

        """
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
        """
        Create a new unclaimed stream.

        An *unclaimed* stream functions just like any other stream, but is not owned by any user, and has no password set. Anyone may post events to an unclaimed stream, but in practice they are private as long as you don't give away the ID.

        :rtype: Stream instance

        >>> my_stream = Stream.new()
        >>> my_stream.text('I just create a new stream!')
        >>> print(my_stream.url)

        """
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
        """Open this stream in your browser."""
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
            'description': event.description,
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
            return AddEventResult(result['event']['url'])

        msg = result.get('msg', 'event error')
        if status == 'ratelimited':
            raise errors.RateLimited(msg)

        raise errors.EventCreateError(result)

    def text(self, text, title="Text", markup="markdown"):
        """Add a text event to this stream.

        >>> my_stream = Stream.new()
        >>> result = my_stream.text('Hello, World!')
        >>> result.browse()

        :param text: The text you want to associate with this event.
        :type text: str
        :param title: The title of the event
        :type title: str
        :rtype: AddEventResult

        """
        event = Event(type="text",
                      title=title,
                      description=text,
                      markup=markup)
        result = self._add_event(event)
        return result

    def code(self, code, language=None, description=None, title="Code", markup="markdown"):
        """Add a (source) code event.

        .. code-block:: python

            with open('example.py') as code_file:
                stream.code(code_file, language="Python")

        :param code: Source code in a string, or an open file like object
        :type code: str or open object
        :param langauge: Programming language.
        :type language: str
        :param description: A description of the source dode.
        :type description: str
        :param title: Title of the Event.
        :type title: str
        :param markup: Markup type for the description.
        :type markup: str
        :rtype: AddEventResult


        """
        if hasattr(code, 'read'):
            code = code.read()
        event = Event(type="code",
                      title=title,
                      markup=markup,
                      description=description,
                      text=code)
        result = self._add_event(event)
        return result

    def image(self, path, description=None, title="New Photo", markup="markdown"):
        """Add an image event.

        :param path: A path to a JPG or PNG.
        :type path: str
        :param description: Description of the image.
        :type description: str
        :param title: Title of the image event.
        :type title: str
        :param markup: Markup used to render description.
        :type markup: str
        :rtype: AddEventResult

        """
        event = Event(type="image",
                      title=title,
                      description=description,
                      markup=markup)
        event.add_image(path)
        result = self._add_event(event)
        return result

    def screenshot(self, delay=0, description=None, title="New Screenshot", markup="markdown"):
        """Take a screenshot and post an event.

        :param delay: Number of seconds to wait before taking the screenshot.
        :type delay: int
        :param description: Description of the screenshot.
        :type description: str
        :param title: Title of the event.
        :type title: str
        :param markup: Markup of the description.
        :type markip: str
        :rtype EventType"

        """
        if delay:
            time.sleep(delay)
        import pyscreenshot
        filename = tempfile.mktemp(prefix='inthing', suffix=".jpg")
        pyscreenshot.grab_to_file(filename)
        event = Event(type="screenshot", title=title, description=description, markup=markup)
        event.add_image(filename)
        result = self._add_event(event)
        return result

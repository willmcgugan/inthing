from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import mimetypes
import os
from os.path import basename
import platform
import sys
import tempfile
import time
import webbrowser

from . import errors
from . import urls
from .compat import text_type
from .event import Event
from .jsonrpc import JSONRPCError
from .rpc import get_interface

import requests


log = logging.getLogger('inthing')


class Result(object):
    """Represents a successfully posted event.

    The ``url`` attribute contains the URL to the the event's page.

    """

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        """Summary with url."""
        return "Result('{}')".format(self.url)

    def browse(self):
        """Open a webbrowser at this event."""
        webbrowser.open(self.url)


class _FileCaptureProxy(object):
    """Proxy a file like object, while intercepting writes."""

    def __init__(self, f, output):
        self._f = f
        self._output = output

    def write(self, data):
        """Hook in to write and store data."""
        self._f.write(data)
        if isinstance(data, bytes):
            data = data.decode(getattr(self._f, 'encoding', None) or 'utf-8', 'replace')
        self._output.append(data)

    def __getattr__(self, k):
        return getattr(self._f, k)


class CaptureContext(object):
    """Context manager to capture stdout/stderr."""

    def __init__(self, stream, title, description=None, stdout=True, stderr=True):
        self.stream = stream
        self.title = title
        self.description = None
        self.result = None
        self.text = None

        self._capture_stdout = stdout
        self._capture_stderr = stderr
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        self._output = []

    def browse(self):
        """Open a browser to the captured data."""
        self.result.browse()

    def __enter__(self):
        """Replace stdout/stderr with proxy objects."""
        if self._capture_stdout:
            sys.stdout = _FileCaptureProxy(sys.stdout, self._output)
        if self._capture_stderr:
            sys.stderr = _FileCaptureProxy(sys.stdout, self._output)
        return self

    def __exit__(self, type, value, tb):
        """Restore stdout/sterr and add event."""
        if self._capture_stdout:
            sys.stdout = self._old_stdout
        if self._capture_stderr:
            sys.stderr = self._old_stderr
        text = ''.join(self._output)
        event = Event(type="code",
                      description=self.description,
                      title=self.title,
                      text=text)
        self.result = self.stream.add_event(event)
        self.text = text


class Stream(object):
    """Inthing Stream class interface.

    This class is the main interface for posting to an Inthing Stream. It represents a single
    Stream, and has methods to post the various event types.

    """

    def __init__(self, id=None, password=None, generator=None, silence_errors=False):
        """Construct a new Stream object.

        :param id: The ID of your stream. This may be either a UUID (mixture of letters an numbers),
            or the URL of the stream.
        :type id: str
        :param password: The stream's password, if required. It's possible for a stream to have no
            password, which allows for anyone to post to it.
        :type password: str
        :param generator: A short string to identify what is creating events.
        :type generator: str
        :param silence_errors: If True, ignore errors when posting events.
        :type silence_errors: bool
        :rtype: Stream

        """
        self.rpc = get_interface()
        self.id = id or os.environ.get('INTHING_STREAM', None)
        self.password = password or os.environ.get('INTHING_STREAM_PASSWORD', None)
        self.generator = platform.node() if generator is None else generator

        if self.id is None:
            raise ValueError('Stream ID or URL is required')

        self.silence_errors = silence_errors
        self.url = None

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

        An *unclaimed* stream functions like any other stream, but is not owned by any user,
        and has no password set. Anyone may post events to an unclaimed stream, but in practice
        they are private as long as you don't give away the ID or URL.

        :rtype Stream:

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

    def capture(self, title="Captured output", description=None, browse=False, stdout=True, stderr=False):
        """Capture stdout and stderr.

        :param title: Title of the captured event
        :type title: str
        :param description: Optional description
        :type description: str
        :param browse: Open a webbrowse to new event?
        :type browse: bool
        :param stdout: Capture stdout?
        :type stdout: bool
        :param stderr: Capture stderr?
        :type stderr: bool


        This method returns a context manager, which will capture ``print`` output, and post it to a stream. Here is an example::

            from inthing import Stream
            stream = Stream.new()
            with stream.capture(title="Capture Example") as capture:
                print('This output will go to a stream!')
            capture.browse()

        """
        return CaptureContext(self,
                              title,
                              description=description,
                              stdout=stdout,
                              stderr=stderr)

    def add_event(self, event):
        """Add an event.

        :param event: Event you want to add.
        :type event: Event

        """
        try:
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
                return Result(result['event']['url'])

            msg = result.get('msg', 'event error')
            if status == 'ratelimited':
                raise errors.RateLimited(msg)

            raise errors.EventFail(result)
        except Exception as e:
            if not self.silence_errors:
                raise
            log.exception('error in add_event')

    def text(self,
             text,
             title="Text",
             markup="markdown",
             priority=0):
        """Add a text event to this stream.

        >>> my_stream = Stream.new()
        >>> result = my_stream.text('Hello, World!')
        >>> result.browse()

        :param text: The text you want to associate with this event.
        :type text: str
        :param title: The title of the event
        :type title: str
        :rtype: Result

        """
        event = Event(type="text",
                      title=title,
                      description=text,
                      markup=markup,
                      priority=priority)
        result = self.add_event(event)
        return result

    def code(self,
             code,
             language=None,
             description=None,
             title="Code",
             markup="markdown",
             priority=0):
        """Add a (source) code event.

        .. code-block:: python

            with open('example.py') as code_file:
                stream.code(code_file, language="Python")

        :param code: Path to a file containing code, or an open file object
        :type code: str or open object
        :param language: Programming language.
        :type language: str
        :param description: A description of the source dode.
        :type description: str
        :param title: Title of the Event.
        :type title: str
        :param markup: Markup type for the description.
        :type markup: str
        :rtype: Result

        """
        if hasattr(code, 'read'):
            code = code.read()
        else:
            with open(code, 'rt') as code_file:
                code = code_file.read()
        if isinstance(code, bytes):
            code = code.decode('utf-8', 'replace')
        event = Event(type="code",
                      title=title,
                      markup=markup,
                      description=description,
                      text=code,
                      code_language=language,
                      priority=priority)
        result = self.add_event(event)
        return result

    def image(self,
              path,
              description=None,
              title="New Photo",
              markup="markdown",
              priority=0):
        """Add an image event.

        :param path: A path to a JPG or PNG.
        :type path: str
        :param description: Description of the image.
        :type description: str
        :param title: Title of the image event.
        :type title: str
        :param markup: Markup used to render description.
        :type markup: str
        :rtype: Result

        """
        event = Event(type="image",
                      title=title,
                      description=description,
                      markup=markup,
                      priority=priority)
        event.add_image(path)
        result = self.add_event(event)
        return result

    def screenshot(self,
                   delay=0,
                   description=None,
                   title="New Screenshot",
                   markup="markdown",
                   priority=0):
        """Take a screenshot and post an event.

        :param delay: Number of seconds to wait before taking the screenshot.
        :type delay: int
        :param description: Description of the screenshot.
        :type description: str
        :param title: Title of the event.
        :type title: str
        :param markup: Markup of the description.
        :type markup: str
        :rtype: Result

        """
        if delay:
            time.sleep(delay)
        import pyscreenshot
        filename = tempfile.mktemp(prefix='inthing', suffix=".jpg")
        pyscreenshot.grab_to_file(filename)
        event = Event(type="screenshot",
                      title=title,
                      description=description,
                      markup=markup,
                      priority=priority)
        event.add_image(filename)
        result = self.add_event(event)
        return result

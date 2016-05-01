
from __future__ import print_function
from __future__ import unicode_literals

import unittest

try:
    import mock
except ImportError:
    from unittest import mock

from inthing import Result, Stream, Event


class TestResult(unittest.TestCase):
    """Test Result object."""

    URL = 'https://www.inthing.io/s/asfasf'

    def test_create(self):
        result = Result(self.URL)
        self.assertEqual(self.URL, result.url)
        self.assertIn(self.URL, repr(result))

    def test_browse(self):
        with mock.patch('webbrowser.open') as webbrowser_open:
            result = Result(self.URL)
            result.browse()
        webbrowser_open.assert_called_with(self.URL)


class TestStream(unittest.TestCase):
    """Test Stream object."""

    def test_create(self):
        stream = Stream('test', password="password", generator="unittest")
        self.assertEqual(stream.id, 'test')
        self.assertEqual(stream.password, 'password')
        self.assertEqual(stream.generator, 'unittest')

    def test_new(self):
        ret = {'id': "ABC", 'password': 'pass', 'url': 'https://example.org'}
        with mock.patch('inthing.jsonrpc.JSONRPC.call', mock.Mock(return_value=ret)):
            stream = Stream.new()
        self.assertEqual(stream.id, ret['id'])
        self.assertEqual(stream.password, ret['password'])
        self.assertEqual(stream.url, ret['url'])

    def test_add_text(self):
        stream = Stream('foo', 'bar')
        with mock.patch('inthing.Stream.add_event') as add_event:
            stream.text('this is the text', title="My Text")
        event = add_event.call_args[0][0]
        assert isinstance(event, Event), 'must be an Event'
        self.assertEqual(event.type, 'text')
        self.assertEqual(event.description, 'this is the text')
        self.assertEqual(event.title, 'My Text')

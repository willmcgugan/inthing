Stream Objects
==============

A stream object is an instance of a :class:`inthing.Stream` and represents a single inthing.io stream. Stream objects may be used to post events to your stream.


Creating Stream Objects
-----------------------

To create a stream object, pass in the URL of the stream as to the Stream constructor as follows::

>>> from inthing import Stream
>>> my_stream = Stream('http://www.inthing.io/will/test/')

Most streams will be protected with a password, which you can pass in with the `password` parameter:

>>> my_stream = Stream('http://www.inthing.io/will/test/', password="daffodil")

You can also use the stream's UUID (universal unique identifier) in place of a URL. The advantage of using a UUID over a URL is that the UUID will never change, but the URL could if you edit the Stream's title. Here's an example of creating a stream object from its UUID::

>>> my_stream = Stream('4d9f242c-0805-11e6-8d28-fb90f1f704e0', password="daffodil")

You can also omit the stream ID / URL and password entirely, if you store the stream ID and password in the environments variables ``INTHING_STREAM`` and ``INTHING_STREAM_PASSWORD``. Which makes constructing a stream object as simple as:

>>> my_stream = Stream()

Unclaimed Streams
-----------------

Alternatively you can create a stream object with `Stream.new`, which creates a new *unclaimed* stream on the server. Here's an example:

>>> my_stream = Stream.new()

Note that unclaimed streams aren't owned by anyone, and you will not see it in your timeline -- but you may still post as normal to it. If you would like to *claim* the stream, you should visit the URL and click the Claim button. You can get the streams URL with the `url` attribute::

>>> print(my_stream.url)

Stream Attributes
-----------------

Stream objects have the following attributes:

* ``stream.url`` The full URL to the stream
* ``stream.id`` The ID of the stream

Posting Events
--------------

You can post an event to your stream with one of the following methods:

* :func:`inthing.Stream.code`
* :func:`inthing.Stream.text`
* :func:`inthing.Stream.image`
* :func:`inthing.Stream.screenshot`

On success you will get back a :class:`inthing.AddEventResult` object, which contains a ``url`` attribute, and a :func:`inthing.AddEventResult.browse` method which will open a browser at the event url.

Here is a very simple (if a little silly) example that creates a new stream, posts a text event, then opens a browser at the event URL:

>>> from inthing import Stream
>>> Stream.new().text('Hello, World!').browse()
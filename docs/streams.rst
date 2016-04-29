.. _streams:

Streams
=======

A stream is a URL on inthing.io with a list of events. You can post to a stream with an instance of a :class:`inthing.stream.Stream` class.

Creating Stream Objects
-----------------------

To create a stream object for an existing stream, pass in the URL of the stream as to the Stream constructor as follows::

>>> from inthing import Stream
>>> my_stream = Stream('https://www.inthing.io/will/test/')

.. note:: You can drop the ``https://www.inthing.io/`` part and just use ``/will/test/`` if you prefer.

Most streams will be protected with a password, which you can pass in with the `password` parameter:

>>> my_stream = Stream('https://www.inthing.io/will/test/', password="daffodil")

Streams also have a UUID (universally unique identifier), which you can use in place of a URL. Here's an example::

>>> my_stream = Stream('4d9f242c-0805-11e6-8d28-fb90f1f704e0', password="daffodil")

Using a UUID has the advantage that it will never change, whereas the URL might, if you change the title.

If you store the stream ID and password in the environments variables ``INTHING_STREAM`` and ``INTHING_STREAM_PASSWORD``, you can omit the arguments from the Stream constructor entirely.

For example, in Linux and OSX, you can do the following from the terminal::

    export INTHING_STREAM=4d9f242c-0805-11e6-8d28-fb90f1f704e0
    export INTHING_STREAM_PASSWORD=daffodil

Then in Python, you can create a stream object as follows::

    from inthing import Stream
    my_stream = Stream()

.. note:: Environment variables also work with Windows, but the process differs from version to version. Ask Google for instructions.

Unclaimed Streams
-----------------

An alternative to creating a stream object for an existing stream, is to call :func:`inthing.Stream.new`, which creates a new stream on the server. Here's an example:

>>> from inthing import Stream
>>> my_stream = Stream.new()
>>> print(my_stream.url)

Stream objects created in this way are *unclaimed*, in that they aren't owned by anyone. You will not see the unclaimed stream in your timeline -- but you may still post events to it as normal. If you would like to *claim* the stream, you should visit the stream's page and click the Claim button. This will attach the stream to your account.

Stream Objects
-----------------

Streams are relatively simple objects. For most applications you will only ever need a single Stream, which you may use to post events.

Streams have the following public attributes:

* ``stream.generator`` A string the identifies the entitiy creating events. The default value for this is the hostname of the computer it is running on. (read/write)
* ``stream.id`` The UUID of the stream. (read only)
* ``stream.url`` The full URL to the stream. (read only)

The :func:`inthing.Stream.browse` method will open a webbrowser the stream page. This does the equivelent of opening a browser and navigating to the URL in ``stream.url``.

The following public methods on stream objects are devoted to posting various kinds of events:

* :func:`inthing.Stream.code`
* :func:`inthing.Stream.text`
* :func:`inthing.Stream.image`
* :func:`inthing.Stream.screenshot`

See :ref:`events` for details.

Rate Limiting
-------------

The inthing.io server imposes a *rate limit* on requests; if you add events too rapidly, the Stream object will throw a :class:`inthing.errors.RateLimited` exception for new events. If this happens, you can wait a while and try again.

This is just a precaution against errors in your code from overloading the server by posting too quickly. The rate limit is high enough that you are unlikely to reach it with functioning code. The server allows for *bursts* of events as long as the number of events averages out within a longer period.

The exact limits are subject to change, but as a general rule, if events are being posted too fast for an average human to read, you may be rate limited.
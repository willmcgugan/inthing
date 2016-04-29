.. _eventtypes:

Event Types
===========

The following is a description of the event types you can post to a stream.

Text
----

A *text* event may contain text for pretty much any purpose.

The following is an example that posts text messages to a stream (Ctrl+C to exit)::

    from inthing import Stream
    stream = Stream.new()
    stream.browse()
    while 1:
        stream.text(raw_input('type something: '))

You could adapt this quite easily to create a realtime chat system on the web.

The ``text`` method also has a ``markup`` parameter which sets the markup for the text. By default it is `markdown <http://commonmark.org/help/>`_, which means you can easily insert formatting. Here's an example::

    stream.text('**Bold** and *italic*')

You can also set the ``markup`` parameter to ``text``, ``bbcode`` or ``html``. But note that Inthing.io will strip out any potentially dangerous HTML markup (so no script tags)!

See :func:`inthing.Stream.screenshot` for details.


Code
----

A *code* event contains source code which you can share and comment on. If you have a piece of code you are particularily proud of, you can post it to Inthing.io. It will be nicely syntax highlighted. A variety of languages are supported.

Here's how you might post source code to a stream::

    my_stream.code('cool.py', language="python", title="I wrote cool.py")

See :func:`inthing.Stream.code` for details.


Image
-----

An *image* event contains an image, typically a photo.

Here's how you would post the file ``alien1.jpg``::

    my_stream.image('./alien1.jpg', description="Alien Autopsy!")

See :func:`inthing.Stream.image` for details.


Screenshots
-----------

A *screenshot* event is a special kind of image event that contains a screenshot. Calling :func:`inthing.Stream.screenshot` will capture a screenshot of your desktop and add the event to your Stream.

Here's how you would upload a screenshot after 5 seconds:

    my_stream.screenshot(self, delay=5, title="My Desktop!")

.. warning:: Be careful with this event, you wouldn't want to screenshot any passwords or nuclear launch codes!

See :func:`inthing.Stream.screenshot` for details.
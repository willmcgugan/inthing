.. _events:

Events
======

Inthing supports a variety of event types, and more are being added. Most of them have common fields; for instance all events will have a ``title`` and probably a ``description``.

When you successfully post an event (with one of the event methods below), you will get back a :class:`inthing.Result` object, which contains a ``url`` attribute, and a :func:`inthing.Result.browse` method which will open a browser at the event url.

Here's an example of using the ``Result`` object::

    from inthing import Stream
    stream = Stream.new()
    result = stream.text('my first event!')
    print("opening {}".format(result.url))
    result.browse()

Priorities
----------

Events have an associated priority value which is an integer between -2 and +2 (inclusive).

.. table:: Priority values

   ===== =======
   Value Meaning
   ===== =======
   +2    Urgent
   +1    Important (of greater than normal signficance)
    0    Normal priority (default)
   -1    Informative
   -2    Verbose
   ===== ======

Markup
------

Most events will have a description field. You can set how the description should be displayed via the `markup` parameter.

.. table:: Supported markups

   ======    =======
   Markup    Meaning
   ======    =======
   text      Simple text
   markdown  `Markdown <http://commonmark.org/>`_.
   html      Simple HTML
   bbcode    `BBCode <https://en.wikipedia.org/wiki/BBCode>`_.

.. note:: Inthing.io will strip descriptions of potentially dangerous markup, such as <script> tags.


Event Types
=============

See the following for the events types you can post to a stram.

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

    with open('cool.py') as code_file:
        my_stream.code(code_file, language="python", title="I wrote cool.py")

See :func:`inthing.Stream.code` for details.


Image
-----

An *image* event contains an image, typically a photo.

Here's how you would post the file ``alien1.jpg``::

    my_stream.image('./alien1.jpg', description="Alien Autopsy!")

See :func:`inthing.Stream.image` for details.


Screenshot
----------

A *screenshot* event is a special kind of image event that contains a screenshot. Calling :func:`inthing.Stream.screenshot` will capture a screenshot of your desktop and add the event to your Stream.

Here's how you would upload a screenshot after 5 seconds:

    my_stream.screenshot(self, delay=5, title="My Desktop!")

.. warning:: Be careful with this event, you wouldn't want to screenshot any passwords or nuclear launch codes!

See :func:`inthing.Stream.screenshot` for details.
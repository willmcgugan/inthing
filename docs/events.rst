.. _events:

Events
======

Inthing supports a variety of **event types**, which display different kinds of information (text, code, images etc) on your stream.

When you successfully post an event with one of the methods in :class:`inthing.Stream`, you will get back a :class:`inthing.Result` object, which contains a ``url`` attribute, and a :func:`inthing.Result.browse` method.

Here's an example of using the ``Result`` object::

    from inthing import Stream
    stream = Stream.new()
    result = stream.text('my first event!')
    print("opening {}".format(result.url))
    result.browse()

See :doc:`eventtypes` for a description of the event types.

Priorities
----------

Events have an associated priority value which is an integer between -2 and +2 (inclusive).

.. table:: Priority values

   ===== ==============================================
   Value Meaning
   ===== ==============================================
   +2    Urgent
   +1    Important (of greater than normal signficance)
   0     Normal priority (default)
   -1    Informative
   -2    Verbose
   ===== ==============================================

Markup
------

Most events will have a description field. You can set how the description should be displayed via the `markup` parameter.

.. table:: Supported markups

   ========  ==================================================
   Markup    Meaning
   ========  ==================================================
   text      Simple text
   markdown  `Markdown <http://commonmark.org/>`_.
   html      Simple HTML
   bbcode    `BBCode <https://en.wikipedia.org/wiki/BBCode>`_.
   ========  ==================================================

.. note:: Inthing.io will strip descriptions of potentially dangerous markup, such as <script> tags.

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


Demo
----

Here's a very simple example that generates an ascii mandlebrot set and posts it to a new Inthing stream::

# demo.py
"""An example of posting a text event to a stream."""

from inthing import Stream


def mandel(xsize=80, ysize=20, max_iteration=50):
    """Render an ascii mandelbrot set!"""
    chars = " .,~:;+*%@##"
    rows = []
    for pixy in xrange(ysize):
        y0 = (float(pixy) / ysize) * 2 - 1
        row = ""
        for pixx in xrange(xsize):
            x0 = (float(pixx) / xsize) * 3 - 2
            x = 0
            y = 0
            iteration = 0
            while (x * x + y * y < 4) and iteration < max_iteration:
                xtemp = x * x - y * y + x0
                y = 2 * x * y + y0
                x = xtemp
                iteration += 1
            row += chars[iteration % 10]
        rows.append(row)
    return "```\n{}\n```\n#mandlebrot".format('\n'.join(rows))


stream = Stream.new()
result = stream.text(mandel(), title="Mandelbrot Set!")
result.browse()

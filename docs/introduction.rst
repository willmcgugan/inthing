Introduction
============

Inthing is a Python module for `<https://inthing.io>`_.

Inthing users create streams of events, which are much like a social media timelines in that they can contain text, rich-media, comments etc., but unlike tranditional social media, Inthing streams are intended primarily for machines to post to via a easy to use API.

How a stream is used and what kind of events are posted to it is entirely up to the developer. It can be used for something as sophisticated as a motion activated camera, or as simple as a one-liner to send a text notification.

Getting Started
---------------

Use PIP to install the Python module::

    pip install inthing

You may need to prefix that with ``sudo`` on some systems.

This will install the ``inthing`` Python module, and also the ``inthing`` command line app. Run the following from the command line to check instalation::

    inthing -v

You will probably also want to create an inthing.io account, which you can do by visiting `<https://inthing.io>`_. Creating an account is *not* a requirement, but will give you more control over your streams.


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

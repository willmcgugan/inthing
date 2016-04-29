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
Command Line App
================

The inthing app is installed with the Python module and can be used to post events directly to a stream via the command line. To check if it is available, run the following::

    inthing -v

You can specify the stream credentials via the environement variables ``INTHING_STREAM`` and ``INTHING_STREAM_PASSWORD``. These can be the same values as used by the the Python :class:`inthing.Stream` object. Here's an example (Linux or OSX)::

    export INTHING_STREAM=https://www.inthing.io/will/test/
    export INTHING_STREAM_PASSWORD=daffodil

You can then one of the available subcommands supported by ``inthing``. The following example posts a simple text event::

    inthing text "Hello, World!" --title "Test Event"

An alternative to using environment variables is to specify the stream and password on the command line as well. Here's an example::

    inthing text "Hello, World!" --title "Test Event" --id https://www.inthing.io/will/test/ --password daffodil

To see the full range of subcommands available, run the following::

    inthing -h

Capturing Output
----------------

The ``capture`` subcommand can be used to capture output from a command and post an event to your stream. Simply *pipe* a command in to ``inthing captue``. Here's an example::

    uptime | inthing capture

This will add a text event containing the output of the ``uptime`` command.

If you add the ``--browse`` switch it will open your browser at the new event, or added the ``--url`` to just display the URL.

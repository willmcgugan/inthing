from __future__ import print_function
from __future__ import unicode_literals

import os

from ..subcommand import SubCommand

from inthing.stream import Stream 


class Event(SubCommand):
    """Add an event to a stream"""

    def add_arguments(self, parser):
        parser.add_argument('--id', dest="id", default=None,
                            help="UUID of stream")
        parser.add_argument('-p', '--password', dest="password", default=None,
                            help="Stream password")
        parser.add_argument('-g', '--generator', dest="generator", default=None,
                            help="Event generator")
        parser.add_argument('-t', '--title', dest="title", required=True,
                            help="Event title")
        parser.add_argument('--text', dest="text",
                            help="Event text")

    def run(self):
        args = self.args

        stream = Stream(id=args.id or os.environ.get('INTHING_STREAM', None),
                        password=args.password or os.environ.get('INTHING_STREAM_PASSWORD', None),
                        generator=args.generator)

        stream.add_text(args.text,
                        title=args.title)
        
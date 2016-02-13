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
        parser.add_argument('--markup', dest='markup', default='markdown',
                            help="Markup to use for text")
        parser.add_argument('--type', dest="type", default='text',
                            help="Take screenshot")
        parser.add_argument('--image', dest="image",
                            help="Path to image file")
        parser.add_argument('--delay', dest="delay", type=int, default=0,
                            help="Delay in taking screenshot")

    def run(self):
        args = self.args

        stream = Stream(id=args.id or os.environ.get('INTHING_STREAM', None),
                        password=args.password or os.environ.get('INTHING_STREAM_PASSWORD', None),
                        generator=args.generator)

        event_type = args.type

        if event_type == 'text':
            stream.text(args.text,
                            title=args.title)
        elif event_type == 'image':
            stream.image(args.image,
                             title=args.title,
                             text=args.text,
                             markup=args.markup)
        elif event_type == 'screenshot':
            stream.screenshot(text=args.text,
                                  title=args.title,
                                  markup=args.markup,
                                  delay=args.delay)
        else:
            self.exit('invalid event type ({})'.format(event_type))
        
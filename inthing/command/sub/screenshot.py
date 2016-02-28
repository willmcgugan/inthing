from __future__ import print_function
from __future__ import unicode_literals

from ..subcommand import EventSubCommand
from ...stream import Stream


class Screenshot(EventSubCommand):
    """Add an event to a stream"""

    def add_arguments(self, parser):
        super(Screenshot, self).add_arguments(parser)
        parser.add_argument('--title', dest="title", required=True,
                            help="Event text")
        parser.add_argument('--text', dest="text",
                            help="Event text")

    def run(self):
        args = self.args

        stream = Stream(id=args.id,
                        password=args.password,
                        generator=args.generator)

        result = stream.screenshot(text=args.text,
                                   title=args.title,
                                   markup=args.markup,
                                   delay=args.delay)
        self.on_result(result)

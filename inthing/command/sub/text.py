from __future__ import print_function
from __future__ import unicode_literals

from ..subcommand import EventSubCommand
from ...stream import Stream 


class Text(EventSubCommand):
    """Add an event to a stream"""

    def add_arguments(self, parser):
        parser.add_argument(dest="text",
                            help="Event text")
        parser.add_argument('-t', '--title', dest="title", required=True,
                            help="Event title")
        super(Text, self).add_arguments(parser)

    def run(self):
        args = self.args

        stream = Stream(id=args.id,
                        password=args.password,
                        generator=args.generator)
     
        result = stream.text(args.text,
                             title=args.title,
                             markup=args.markup)

        self.on_result(result)


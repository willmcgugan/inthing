from __future__ import print_function
from __future__ import unicode_literals

from ..subcommand import EventSubCommand


class Text(EventSubCommand):
    """Add an event to a stream."""

    def add_arguments(self, parser):
        super(Text, self).add_arguments(parser)
        parser.add_argument(dest="text",
                            help="Event text")

    def run(self):
        args = self.args

        result = self.stream.text(args.text,
                                  title=args.title,
                                  markup=args.markup)

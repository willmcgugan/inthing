from __future__ import print_function
from __future__ import unicode_literals

from ..subcommand import EventSubCommand


class Screenshot(EventSubCommand):
    """Add an event to a stream."""

    def add_arguments(self, parser):
        super(Screenshot, self).add_arguments(parser)
        parser.add_argument('--image', dest="image",
                            help="Path to image file")
        parser.add_argument('--delay', dest="delay", type=int, default=0,
                            help="Delay in taking screenshot")

    def run_event(self):
        args = self.args
        result = self.stream.screenshot(text=args.description,
                                        title=args.title or 'Screenshot',
                                        markup=args.markup,
                                        delay=args.delay)
        return result

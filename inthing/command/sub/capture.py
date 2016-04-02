from __future__ import print_function
from __future__ import unicode_literals

import locale
import sys

from ..subcommand import EventSubCommand

from inthing.stream import Stream


class Capture(EventSubCommand):
    """Capture output to a inthing Stream."""

    def add_arguments(self, parser):
        super(Capture, self).add_arguments(parser)
        parser.add_argument('-t', '--title', dest="title", required=False,
                            help="Event title", default=None)

    def run(self):
        args = self.args

        stream = Stream(id=args.id,
                        password=args.password,
                        generator=args.generator)

        text = sys.stdin.read()

        if isinstance(text, bytes):
            encoding = sys.stdin.encoding or locale.getdefaultlocale()[1]
            text = text.decode(encoding, 'replace')

        result = stream.text("```\n{}\n```\n".format(text),
                             markup="markdown",
                             title=args.title or "Capture")

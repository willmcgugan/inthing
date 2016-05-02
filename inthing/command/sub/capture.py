from __future__ import print_function
from __future__ import unicode_literals

import locale
import sys

from ..subcommand import EventSubCommand

from inthing import Stream, Event


class Capture(EventSubCommand):
    """Capture output to a inthing Stream."""

    help = "capture stdin and post a text event"

    MAX_CHARS = 64 * 1024 - 20

    def add_arguments(self, parser):
        super(Capture, self).add_arguments(parser)
        parser.add_argument('-l', '--language', dest="language", required=False,
                            help="Programming language (if catting code)")

    def run_event(self):
        args = self.args

        stream = Stream(id=args.id,
                        password=args.password,
                        generator=args.generator)

        encoding = sys.stdin.encoding or locale.getdefaultlocale()[1]

        char_count = 0
        lines = []
        for line in sys.stdin:
            sys.stdout.write(line)
            line = line.decode(encoding, 'replace')
            if char_count + len(line) <= self.MAX_CHARS:
                lines.append(line)
            char_count += len(line)

        text = "".join(lines)[:self.MAX_CHARS]
        if isinstance(text, bytes):
            encoding = sys.stdin.encoding or locale.getdefaultlocale()[1]
            text = text.decode(encoding, 'replace')

        event = Event(type="code",
                      title=args.title or 'Capture Event',
                      markup=args.markup,
                      description=args.description,
                      text=text)

        result = stream.add_event(event)
        return result

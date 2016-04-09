from __future__ import print_function
from __future__ import unicode_literals

import locale
import sys

from ..subcommand import EventSubCommand

from inthing.stream import Stream


class Capture(EventSubCommand):
    """Capture output to a inthing Stream."""

    MAX_CHARS = 64 * 1024 - 20

    def add_arguments(self, parser):
        super(Capture, self).add_arguments(parser)
        parser.add_argument('-l', '--language', dest="language", required=False,
                            help="Programming language (if catting code)")

    def run(self):
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

        result = stream.text(text,
                             type="code",
                             code_language=args.language,
                             title=args.title or "Capture")

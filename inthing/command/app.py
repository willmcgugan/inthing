from __future__ import unicode_literals
from __future__ import print_function

import sys
import argparse
import importlib


from .sub import __all__ as SUBCOMMANDS
from .subcommand import SubCommandMeta
from ..compat import text_type
from .. import __version__ as version


class Inthing(object):
    """inthing command line app."""

    def __init__(self):
        self.subcommands = {}

    def make_subcommands(self):
        self.subcommands = {name: cls(self)
                            for name, cls in SubCommandMeta.registry.items()}

    def get_argparse(self):
        parser = argparse.ArgumentParser(description="Client for inthing.io")

        parser.add_argument('-v', '--version', action='version', version=version)
        parser.add_argument('-d', '--debug', dest="debug", action="store_true", default=False,
                            help='enables debug output')

        subparsers = parser.add_subparsers(title='available sub-commands',
                                           dest="subcommand",
                                           help="sub-command help")

        for name, subcommand in sorted(self.subcommands.items(), key=lambda item: item[0]):
            subparser = subparsers.add_parser(name,
                                              help=subcommand.help,
                                              description=getattr(subcommand, '__doc__', None))
            subcommand.add_arguments(subparser)

        return parser

    def run(self):
        for name in SUBCOMMANDS:
            importlib.import_module('.' + name, 'inthing.command.sub')
        self.make_subcommands()
        parser = self.get_argparse()
        self.args = parser.parse_args(sys.argv[1:])

        if self.args.subcommand is None:
            parser.print_usage()
            return 1

        subcommand = self.subcommands[self.args.subcommand]
        subcommand.args = self.args

        try:
            return subcommand.run()
        except Exception as e:
            if self.args.debug:
                import traceback
                traceback.print_exc(e)
            else:
                if hasattr(e, 'print_error'):
                    e.print_error()
                else:
                    sys.stderr.write("{}\n".format(text_type(e)))
            return -1

    def error(self, msg):
        sys.stderr.write(msg + '\n')


def main():
    inthing = Inthing()
    return inthing.run()

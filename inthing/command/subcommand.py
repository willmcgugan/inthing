from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys

from ..compat import with_metaclass
from ..stream import Stream


class SubCommandMeta(type):
    registry = {}

    def __new__(cls, name, base, attrs):
        new_class = type.__new__(cls, name, base, attrs)
        if name not in ("SubCommand", "EventSubCommand"):
            cls.registry[name.lower()] = new_class
        return new_class


class SubCommandType(object):
    help = ''
    description = ''

    def __init__(self, command):
        self.command = command

    def add_arguments(self, parser):
        pass

    def debug(self, text):
        return self.command.debug(text)

    def error(self, text):
        return self.command.error(text)

    def exit(self, msg='', code=-1):
        if msg:
            self.error(msg)
        sys.exit(code)

    def run():
        pass


class SubCommand(with_metaclass(SubCommandMeta, SubCommandType)):
    pass


class EventSubCommand(SubCommand):

    def add_arguments(self, parser):
        parser.add_argument('--id', dest="id", default=None,
                            help="ID of stream")
        parser.add_argument('-p', '--password', dest="password", default=None,
                            help="Stream password")
        parser.add_argument('-g', '--generator', dest="generator", default=None,
                            help="Event generator")

        parser.add_argument('-t', '--title', dest="title", required=True,
                            help="Event title")
        parser.add_argument('-d', '--description', dest="description",
                            help="Event description")
        parser.add_argument('-m', '--markup', dest='markup', default='markdown',
                            help="Markup to use for text")

    @property
    def stream(self):
        if getattr(self, '_stream', None):
            return self._stream

        args = self.args
        stream = Stream(id=args.id or os.environ.get('INTHING_STREAM', None),
                        password=args.password or os.environ.get('INTHING_STREAM_PASSWORD', None),
                        generator=args.generator)
        return stream

    def on_result(self, result):
        #print(result)
        if result.get('status') == 'fail':
            sys.stderr.write(result.get('msg') + '\n')
            for field, errors in result.get('field_errors', {}).items():
                sys.stderr.write(" * {} - {}\n".format(field, ', '.join(errors)))

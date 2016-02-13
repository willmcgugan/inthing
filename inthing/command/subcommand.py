from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from ..compat import with_metaclass

import sys

class SubCommandMeta(type):
    registry = {}

    def __new__(cls, name, base, attrs):
        new_class = type.__new__(cls, name, base, attrs)
        if name != "SubCommand":
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
        parser.add_argument('--markup', dest='markup', default='markdown',
                            help="Markup to use for text")
        parser.add_argument('--image', dest="image",
                            help="Path to image file")
        parser.add_argument('--delay', dest="delay", type=int, default=0,
                            help="Delay in taking screenshot")

    def on_result(self, result):
        #print(result)
        if result.get('status') == 'fail':
            sys.stderr.write(result.get('msg') + '\n')
            for field, errors in result.get('field_errors', {}).items():
                sys.stderr.write(" * {} - {}\n".format(field, ', '.join(errors)))

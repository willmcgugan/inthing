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

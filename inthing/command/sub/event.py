from __future__ import print_function
from __future__ import unicode_literals

from ..subcommand import SubCommand


class Event(SubCommand):
	"""Add an event to a stream"""

	def add_arguments(self, parser):
		parser.add_argument('-t', '--title', dest="title",
							help="Event title")
		parser.add_argument('--text', dest="text",
							help="Event text")

	def run(self):
		args = self.args
		print(args)
from __future__ import unicode_literals
from __future__ import print_function

from . import rpc
from . import errors
from .compat import text_type
from .jsonrpc import JSONRPCError


class Stream(object):
	"""A stream of events"""
	
	def __init__(self):
		self.rpc = rpc.get_interface()
		self.id = None
		self.url = None
		super(Stream, self).__init__()

		self._new()

	def __repr__(self):
		if self.url is None:
			return "<stream>"
		else:
			return "<stream {}>".format(self.url)

	def _new(self):
		try:
			result = self.rpc.call('stream.new')
		except JSONRPCError as e:
			raise errors.StreamError(text_type(e))
		else:
			self.id = result['uuid']
			self.url = result['url']

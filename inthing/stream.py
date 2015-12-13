from __future__ import unicode_literals
from __future__ import print_function

from . import rpc
from . import errors
from .compat import text_type
from .jsonrpc import JSONRPCError

import json

class Stream(object):
	"""A stream of events"""
	
	def __init__(self, id=None, password=None):
		self.rpc = rpc.get_interface()
		self.id = None
		self.url = None
		super(Stream, self).__init__()

		if id is not None:
			self._get(id, password)
		else:
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

	def _get(self, stream, password):
		try:
			result = self.rpc.call('stream.get', stream=id, password=id)
		except JSONRPCError as e:
			raise errors.StreamError(text_type(e))
		self.id = result['uuid']
		self.url = result['url']

	def _new_event(self, event):
		return self._new_events([event])

	def _new_events(self, events):

		event_data = [event.get_event_data() for event in events]
		
		results = self.rpc.call('event.new', stream=self.id, events=event_data)
		for event, event_id in zip(events, results['ids']):
			event.id = event_id or event.id

	def add(self, event):
		event.set_stream(self)
		event.save()


		


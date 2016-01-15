from __future__ import print_function
from __future__ import unicode_literals


class Event(object):
	def __init__(self, title, type="text", priority=0, markup="markdown", text="", generator=None):
		self.title = title
		self.type = type
		self.priority = priority
		self.markup = markup
		self.text = text
		self.generator = generator

		self.id = None
		self.images = []

	def add_image(self, path):
		self.images.append(path)

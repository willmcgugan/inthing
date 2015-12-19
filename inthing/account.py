class Account(object):

	def __init__(self, username, password):
		self.username = username
		self._validated = False
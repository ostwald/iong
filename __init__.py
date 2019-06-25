__author__ = 'ostwald'

from UserDict import UserDict

class WarningUserDict (UserDict):

	def __getitem__ (self, key):
		if not self.data.has_key(key):
			print 'WARN: key not found for {}'.format(key)
			return None
		return self.data[key]


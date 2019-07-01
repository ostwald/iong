__author__ = 'ostwald'

import os
import sys

sys.path.append ('/Users/ostwald/devel/python-lib')

from tabdelimited import CsvFile


class SchemaReporter (CsvFile):

	linesep = '\r'

	def __init__ (self, path):
		CsvFile.__init__(self)
		self.path = path
		self.read(self.path)
		print '%d records read' % len(self.data)
		self.report_schema()

	def preprocess (self, filecontents):
		return filecontents

	def report_schema(self):
		print 'SCHEMA REPORT - {}'.format(os.path.basename(self.path))

		for field in self.schema:
			print '-', field

if __name__ == '__main__':
	path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/Customers_selected_fields.csv'
	SchemaReporter (path)
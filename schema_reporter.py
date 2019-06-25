__author__ = 'ostwald'

import sys, os

sys.path.append ('/Users/ostwald/devel/python/python-lib')

from tabdelimited import CsvFile, FieldList, CsvRecord

from order_detail_reader import OrderDetailReader
from customer_reader import CustomerReader

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
	path = '/Users/ostwald/Documents/people/Karen/IONG_Orders/select_fields/Orders_selected_fields.csv'
	SchemaReporter (path)
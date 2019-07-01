"""
OrdersReader needs access to OrderDetailReader ...
"""

import os, sys, re

sys.path.append ('/Users/ostwald/devel/python/python-lib')

from tabdelimited import CsvFile, FieldList, CsvRecord
from order_detail_reader import OrderDetailReader
from customer_reader import CustomerReader

class OrderRecord (CsvRecord):

	def __init__ (self, data, parent):
		CsvRecord.__init__(self, data, parent)


class OrdersReader (CsvFile):
	record_constructor = OrderRecord
	linesep = '\r'

	def __init__ (self, path):
		CsvFile.__init__(self)
		self.read(path)



if __name__ == '__main__':

	path = '/Users/ostwald/Documents/people/Karen/IONG_Orders/test/Orders_test.csv'
	reader = OrdersReader (path)
	print '%d records read' % len(reader)
	# print csvFile.schema

	for order in reader.data:
		print order
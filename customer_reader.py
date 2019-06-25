import os, sys, re


sys.path.append ('/Users/ostwald/devel/python/python-lib')
sys.path.append ('/Users/ostwald/devel')

from UserDict import UserDict
from iong import WarningUserDict
from tabdelimited import CsvFile, FieldList, CsvRecord, TabDelimitedFile, TabDelimitedRecord


class CustomerRecord (CsvRecord):

	def __repr__ (self):
		s = unicode()
		s += "Customer {} ({})".format(self['emailaddress'], self['customerid'])
		s += '\n\t{}, {}'.format(self['lastname'], self['firstname'])
		return s

class CustomerReader (CsvFile):
	record_constructor = CustomerRecord
	linesep = '\r'

	def __init__ (self, path):
		CsvFile.__init__(self)
		self.read(path)
		self.customer_id_map = WarningUserDict()
		for rec in self.data:
			self.customer_id_map[rec['customerid']] = rec

	def get_customer (self, customer_id):
		return self.customer_id_map[customer_id]

	def preprocess (self, filecontents):
		return filecontents


if __name__ == '__main__':

	path = '/Users/ostwald/Documents/people/Karen/IONG_Orders/Customers_ALL.csv'
	reader = CustomerReader (path)
	print '%d records read' % len(reader)
	# print reader.schema

	# for c in reader.data:
	# 	print c

	c = reader.get_customer(unicode('22198'))
	print c


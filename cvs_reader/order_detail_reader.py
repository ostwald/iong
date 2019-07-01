import os, sys, re
from UserDict import UserDict

sys.path.append ('/Users/ostwald/devel/python/python-lib')

from tabdelimited import CsvFile, FieldList, CsvRecord, TabDelimitedFile, TabDelimitedRecord


class OrderDetailRecord (CsvRecord):

	def __repr__ (self):
		s = "OrderDetail {}".format(self['orderdetailid'])
		s += '\t{} ({}) - x{}'.format(self['productname'], self['productcode'], self['quantity'])
		return s

class OrderDetailReader (CsvFile):
	record_constructor = OrderDetailRecord
	linesep = '\r'

	def __init__ (self, path):
		CsvFile.__init__(self)
		self.read(path)
		order_id_map = UserDict()
		order_detail_id_map = {}
		for rec in self.data:

			order_detail_id_map[rec['orderdetailid']] = rec

			order_id = rec['orderid']
			val = order_id_map.has_key(order_id) and order_id_map[order_id] or []
			val.append (rec['orderdetailid'])
			order_id_map[order_id] = val
		self.order_id_map = order_id_map
		self.order_detail_id_map = order_detail_id_map

	def get_details (self, order_detail_id):
		if not self.order_detail_id_map.has_key(order_detail_id):
			print 'WARN: order_detail_id_map does not have key {}'.format(order_detail_id)
			return None
		return self.order_detail_id_map[order_detail_id]

	def get_item_ids (self, order_id):
		if not self.order_id_map.has_key(order_id):
			print 'WARN: get_item_ids doe not have key {}'.format(order_id)
			return None
		return self.order_id_map[order_id]

	def preprocess (self, filecontents):
		return filecontents

if __name__ == '__main__':

	path = '/Users/ostwald/Documents/people/Karen/IONG_Orders/test/OrderDetails_test.csv'
	path = '/Users/ostwald/Documents/people/Karen/IONG_Orders/OrderDetails_since_2016_05_16.csv'
	reader = OrderDetailReader (path)
	print '%d records read' % len(reader)
	# print reader.schema

	# rec = reader.data[0]
	# print rec
	# for field in rec.parent.schema:
	# 	print '- {}  - {}'.format(field, rec[field])

	for order_id in sorted (reader.order_id_map.keys()):
		# print ' - {} - {}'.format(key, reader.order_id_map[key])
		# continue
		print ' - order_id {}'.format(order_id)
		for item_id in reader.get_item_ids(order_id):
			item = reader.get_details(item_id)
			print '\t{}'.format(item)

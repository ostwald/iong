__author__ = 'ostwald'

from UserDict import UserDict
from orders_table import OrdersTable
from order_details_table import OrderDetailsTable
from customers_table import CustomersTable




class WarningUserDict (UserDict):

	def __getitem__ (self, key):
		if not self.data.has_key(key):
			print 'WARN: key not found for {}'.format(key)
			return None
		return self.data[key]


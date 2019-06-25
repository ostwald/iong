import sys, os, re, time

sys.path.append ('/Users/ostwald/devel/python-lib/')

from jloFS import JloFile
from UserDict import UserDict
from UserList import UserList


from orders_reader import OrdersReader
import sqlite3
from ion_db import DBTable, Schema

class OrdersDb (DBTable):
    sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
    table_name = 'orders'

    def __init__(self, order_reader):
        self.order_reader = order_reader
        self.schema = self.make_schema()
        # DBTable.__init__(self)

        for row in order_reader.data[:5]:
            self.add_record(row)

    def make_schema (self):
        print "HELLO"
        schema_spec = []
        for field in self.order_reader.schema:
            schema_spec.append([field, 'TEXT', lambda x:x[field]])

        print schema_spec
        return Schema (schema_spec)



if __name__ == '__main__':
    path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/since_2016/Orders.csv'
    order_reader = OrdersReader (path)
    print '%d records read' % len(order_reader)
    db = OrdersDb(order_reader)
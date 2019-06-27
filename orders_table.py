import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')

from UserDict import UserDict
from UserList import UserList


import sqlite3
from ion_table import DBTable, DBRecord
import schemas

class OrderRecord(DBRecord):
    schema_fields = schemas.order

class OrdersTable (DBTable):

    schema_fields = schemas.order
    sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
    table_name = 'orders'

    def get_order (self, orderid):
        query = "SELECT *  FROM `{tn}` WHERE orderid = '{id}'"\
                .format(tn=self.table_name, id=orderid)

        # print total_query

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return OrderRecord(row)

    def get_order_ids(self, sort_by='orderdate', order='ASC'):
        query = "SELECT orderid FROM {} ORDER BY '{}' {}"\
            .format(self.table_name, sort_by, order)

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return map(lambda x:x[0], rows)

def get_order_tester():
    table = OrdersTable()

    order = table.get_order('29620')

    for field in order.schema:
        print '- {} : {}'.format(field, order[field])

    print json.dumps(order.asDict())

if __name__ == '__main__':
    table = OrdersTable()

    orders = table.get_order_ids()

    j = {}
    for orderid in orders:
        j[orderid] = table.get_order(orderid).asDict()

    fp = open ("JSON_TESTER.json", 'w')
    fp.write (json.dumps(j))
    fp.close()
    print 'json written'

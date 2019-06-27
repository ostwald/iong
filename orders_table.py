import sys, os, re, time

sys.path.append ('/Users/ostwald/devel/python-lib/')

from UserDict import UserDict
from UserList import UserList


import sqlite3
from ion_table import DBTable, DBRecord
import schemas

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

        return DBRecord(row, self.schema)



if __name__ == '__main__':
    table = OrdersTable()

    order = table.get_order('29620')

    for field in order.schema:
        print '- {} : {}'.format(field, order[field])
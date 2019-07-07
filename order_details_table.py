import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')

from UserDict import UserDict
from UserList import UserList


import sqlite3
from ion_table import DBTable, DBRecord
import schemas

class OrderDetailsRecord(DBRecord):
    schema_fields = schemas.order_details

class OrderDetailsTable (DBTable):

    sqlite_file = schemas.sqlite_file

    schema_fields = schemas.order_details
    # sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
    # sqlite_file = '/Users/ostwald/devel/projects/iong/ion_db.sqlite'
    table_name = 'order_details'

    def get_order_details (self, orderid):
        query = "SELECT *  FROM `{tn}` WHERE orderid = '{id}'"\
                .format(tn=self.table_name, id=orderid)

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        return map (OrderDetailsRecord, rows)

    def get_order_details_asDict(self, orderId):

        details = table.get_order_details('29651')

        data_list = []
        for detail in details:
            data_list.append(detail.asDict())

        return {'order_details': data_list}

def get_details_tester(orderId):
    table = OrderDetailsTable()
    details = table.get_order_details_asDict (orderId)
    print json.dumps (details, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    details = get_details_tester('29651')


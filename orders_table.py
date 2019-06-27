import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')


from ion_table import DBTable, DBRecord
from order_details_table import OrderDetailsTable
import schemas

class OrderRecord(DBRecord):
    schema_fields = schemas.order

class OrdersTable (DBTable):

    schema_fields = schemas.order
    # sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
    sqlite_file = 'ion_db.sqlite'
    table_name = 'orders'

    def get_order (self, orderid):
        query = "SELECT *  FROM `{tn}` WHERE orderid = '{id}'"\
                .format(tn=self.table_name, id=orderid)

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


def get_orders_asJson():
    orders_table = OrdersTable()
    orders = orders_table.get_order_ids()

    order_details_table = OrderDetailsTable()

    j = {}
    for orderid in orders[:100]:
        j[orderid] = orders_table.get_order(orderid).asDict()
        details = order_details_table.get_order_details(orderid)
        j[orderid]['order_details'] = []
        for obj in details:
            j[orderid]['order_details'].append(obj.asDict())


    fp = open ("JSON_TESTER.json", 'w')
    fp.write (json.dumps(j, sort_keys=False, indent=4, separators=(',', ': ')))
    fp.close()
    print 'json written'

if __name__ == '__main__':
    get_orders_asJson()

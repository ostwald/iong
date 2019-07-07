import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')


from ion_table import DBTable, DBRecord
from order_details_table import OrderDetailsTable
import schemas

class OrderRecord(DBRecord):
    schema_fields = schemas.order

class OrdersTable (DBTable):

    schema_fields = schemas.order
    # sqlite_file = '/Users/ostwald/devel/projects/iong/ion_db.sqlite'
    sqlite_file = schemas.sqlite_file
    table_name = 'orders'

    def get_order (self, orderid):
        query = "SELECT *  FROM `{tn}` WHERE orderid = '{id}'"\
                .format(tn=self.table_name, id=orderid)

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return OrderRecord(row)

    def get_order_ids(self, sort_by='orderdate', order='ASC', date_range=None):
        query = "SELECT orderid FROM {}".format(self.table_name)

        if date_range:
            query += " WHERE orderdate > '{}' AND orderdate < '{}'" \
                .format (date_range['start'], date_range['end'])

        query += " ORDER BY '{}' {}".format(sort_by, order)


        print "QUERY", query

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return map(lambda x:x[0], rows)

def get_order_tester():
    table = OrdersTable()

    order = table.get_order('29620')

    for field in order.schema:
        print '- {} : {}'.format(field, order[field])

    print json.dumps(order.asDict())


def get_orders_by_date():
    orders_table = OrdersTable()
    orders = orders_table.get_order_ids(sort_by='orderdate')

    order_details_table = OrderDetailsTable()

    j = []
    for orderid in orders[:100]:
        order = orders_table.get_order(orderid).asDict()
        details = order_details_table.get_order_details(orderid)
        obj_json = {
            'orderdate':order['orderdate'],
            'order' : order,
            'details' : [],
        }
        for d in details:
            obj_json['details'].append (d.asDict())
        j.append(obj_json)

    fp = open ("ORDERS_BY_DATE.json", 'w')
    fp.write (json.dumps(j, sort_keys=False, indent=4, separators=(',', ': ')))
    fp.close()
    print 'json written'

if __name__ == '__main__':
    get_orders_by_date()

import sys, os, re, time, json, datetime

sys.path.append ('/Users/ostwald/devel/projects/')
sys.path.append ('/Users/ostwald/devel/')

from iong import schemas

sys.path.append (schemas.python_lib_dir)

from iong import OrdersTable, OrderDetailsTable, CustomersTable
from iong import utils

"""
SELECT orderid, customerid, orderdate FROM orders where orderdate > '2/2/16' AND orderdate < '4/1/16';
"""

def write_orders_by_date():
    orders_table = OrdersTable()
    customers_table = CustomersTable()
    order_details_table = OrderDetailsTable()

    orders = orders_table.get_order_ids(sort_by='orderdate')

    j = []
    for orderid in orders:
        order = orders_table.get_order(orderid).asDict()
        details = order_details_table.get_order_details(orderid)
        try:
            customer = customers_table.get_customer(order['customerid']).asDict()
        except:
            print 'customer not found for order: {} ({})'.format(orderid, order['customerid'])
            customer = {}

        obj_json = {
            'orderdate':order['orderdate'],
            'order' : order,
            'customer' : customer,
            'details' : [],
        }
        for d in details:
            obj_json['details'].append (d.asDict())
        j.append(obj_json)

    filename = "ORDERS_BY_DATE.json"
    filepath = os.pat.join (schemas.json_sandbox, filename)
    fp = open (filename, 'w')
    fp.write (json.dumps(j, sort_keys=False, indent=4, separators=(',', ': ')))
    fp.close()
    print 'json written'

class OrderByDateWriter:

    sandbox_dir = schemas.json_sandbox

    def __init__ (self):
        self.orders_table = OrdersTable()
        self.customers_table = CustomersTable()
        self.order_details_table = OrderDetailsTable()
        self.orders_json = None

    def get_orders_json (self, start, end):
        date_range = {'start':start, 'end':end}
        orders = self.orders_table.get_order_ids(sort_by='orderdate', date_range=date_range)

        orders_json = []
        for orderid in orders[:200]:
            order = self.orders_table.get_order(orderid).asDict()
            details = self.order_details_table.get_order_details(orderid)
            try:
                customer = self.customers_table.get_customer(order['customerid']).asDict()
            except:
                print 'customer not found for order: {} ({})'.format(orderid, order['customerid'])
                customer = {}

            obj_json = {
                'orderdate':order['orderdate'],
                'order' : order,
                'customer' : customer,
                'details' : [],
            }
            for d in details:
                obj_json['details'].append (d.asDict())
            orders_json.append(obj_json)

        return orders_json

    def write_month_orders_json (self, start):
        """
        start is of form YYYY-MM-DD
        """
        end = utils.get_first_of_next_month(start)
        orders_json = self.get_orders_json (start, end)
        outpath = os.path.join (self.json_data_dir, 'orders_by_date', start + '.json')
        self.write_orders_json(orders_json, outpath)

    def write_orders_json (self, data_json, path):
        fp = open (path, 'w')
        fp.write (json.dumps(data_json, sort_keys=False, indent=4, separators=(',', ': ')))
        fp.close()
        print 'json written to {}'.format(path)

def write_batched_orders_by_date():
    start_day = '2016-01-01'
    end_day = '2017-01-01'

    writer = OrderByDateWriter()

    while start_day < end_day:
        print start_day
        writer.write_month_orders_json(start_day)
        start_day = utils.get_first_of_next_month(start_day)

def write_tester():
    start = '2017-12-01'
    end = '2017-12-31'

    writer = OrderByDateWriter()
    orders_json = writer.get_orders_json (start, end)
    outpath = os.path.join (schemas.json_sandbox, 'ORDERS_BY_DATE.json')
    writer.write_orders_json(orders_json, outpath)

if __name__ == '__main__':
    # write_batched_orders_by_date()

    write_tester()
    # write_orders_by_date()

    # writer = OrderByDateWriter()
    # orders_json = writer.write_month_orders_json('2016-03-01')

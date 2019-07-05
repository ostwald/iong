import sys, os, re, time, json, datetime

sys.path.append ('/Users/ostwald/devel/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects/')


from iong import OrdersTable, OrderDetailsTable, CustomersTable
from iong import schemas
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
    for orderid in orders[:1000]:
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

    fp = open ("ORDERS_BY_DATE.json", 'w')
    fp.write (json.dumps(j, sort_keys=False, indent=4, separators=(',', ': ')))
    fp.close()
    print 'json written'

class OrderByDateWriter:

    def __init__ (self):
        self.orders_table = OrdersTable()
        self.customers_table = CustomersTable()
        self.order_details_table = OrderDetailsTable()
        self.orders_json = None

    def write_month_orders_json (self, month, year):
        start = "1/{}/{}".format(month, year)
        end = utils.get_first_of_next_month(start)
        return self.get_orders_json (start, end)

    def get_orders_json (self, start, end):
        date_range = {'start':start, 'end':end}
        orders = self.orders_table.get_order_ids(sort_by='orderdate', date_range=date_range)

        sys.exit()

        orders_json = []
        for orderid in orders[:1000]:
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

        outpath = os.path.join ('orders_per_month', utils.get_iso_day(start) + '.json')
        self.write_orders_json(orders_json, outpath)

        return orders_json


    def write_orders_json (self, data_json, path):
        fp = open (path, 'w')
        fp.write (json.dumps(data_json, sort_keys=False, indent=4, separators=(',', ': ')))
        fp.close()
        print 'json written'

def write_batched_orders_by_date():
    import datetime
    start_day = '1/1/16'
    end_day = '6/30/19'

    for i in range (1,14):
        print start_day
        start_day = utils.get_first_of_next_month(start_day)


if __name__ == '__main__':
    #write_batched_orders_by_date()
    # write_orders_by_date()

    writer = OrderByDateWriter()
    orders_json = writer.write_month_orders_json('3','16')

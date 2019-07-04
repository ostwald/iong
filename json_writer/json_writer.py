import sys, os, re, time, json, datetime
from dateutil.relativedelta import *

sys.path.append ('/Users/ostwald/devel/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects/')


from iong import OrdersTable, OrderDetailsTable, CustomersTable
import iong.schemas

"""
SELECT orderid, customerid, orderdate FROM orders where orderdate > '2/2/16' AND orderdate < '4/1/16';
"""

def write_orders_by_date():
    orders_table = OrdersTable()
    customers_table = CustomersTable()
    orders = orders_table.get_order_ids(sort_by='orderdate')

    order_details_table = OrderDetailsTable()

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

def get_first_of_next_month (date_str):
    fmt = '%m/%d/%y'

    n = datetime.datetime.strptime(date_str,fmt)
    n = n + relativedelta(months=+1)

    return n.strftime (fmt)

def write_batched_orders_by_date():
    import datetime
    start_day = '1/1/16'
    end_day = '6/30/19'

    for i in range (1,14):
        print start_day
        start_day = get_first_of_next_month(start_day)


if __name__ == '__main__':
    write_batched_orders_by_date()
    # write_orders_by_date()
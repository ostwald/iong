import sys, os, re, time, json

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

if __name__ == '__main__':
    write_orders_by_date()
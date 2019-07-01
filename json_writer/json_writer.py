import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects/')


from iong import OrdersTable, OrderDetailsTable, CustomersTable
import schemas


def get_orders_by_date():
    orders_table = OrdersTable()
    customers_table = CustomersTable()
    orders = orders_table.get_order_ids(sort_by='orderdate')

    order_details_table = OrderDetailsTable()

    j = []
    for orderid in orders[:100]:
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
    get_orders_by_date()
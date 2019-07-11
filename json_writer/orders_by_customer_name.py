import sys, os, re, time, json, datetime

sys.path.append ('/Users/ostwald/devel/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects/')
sys.path.append ('/Users/ostwald/devel/')


from iong import OrdersTable, OrderDetailsTable, CustomersTable
from iong import schemas
from iong import utils

"""
select * from customers where UPPER(lastname) < 'A' ORDER BY lastname, firstname ASC

select * from customers where UPPER(lastname) LIKE 'A%' ORDER BY UPPER(lastname), UPPER(firstname) ASC
"""

class OrderByCustomerWriter:

    def __init__ (self):
        self.orders_table = OrdersTable()
        self.customers_table = CustomersTable()
        self.order_details_table = OrderDetailsTable()
        self.orders_json = None


    def get_customers(self, where_clause):
        """
            e.g.
            - UPPER(lastname) < 'A'
            - UPPER(lastname) LIKE 'A%'

        """
        order_by = "UPPER(lastname), UPPER(firstname)"
        return self.customers_table.get_customers(where=where_clause, order_by=order_by)

    def get_orders_json (self, where_clause):

        customers = self.get_customers(where_clause)

        orders_json = []
        for customer in customers:
            customer_json = {'customer': customer.asDict(), 'orders' : []}
            orders = self.orders_table.get_orders_by_customer(customer['customerid'])

            for order in orders:
                order_json = {'order': order.asDict(), 'details': []}
                customer_json['orders'].append (order_json)

                details = self.order_details_table.get_order_details(order['orderid'])
                for detail in details:
                    order_json['details'].append (detail.asDict())

            orders_json.append(customer_json)

        return orders_json

    def write_orders_batch_json (self, where_clause):
        """
        start is of form YYYY-MM-DD
        """

        pat = re.compile ("UPPER\(lastname\) LIKE \'([A-Z])\%\'")
        m = pat.match (where_clause)
        if not m:
            raise Exception ('Could not parse where clause: ({})'.format(where_clause))
        where_letter = m.group(1)

        orders_json = self.get_orders_json(where_clause)
        outpath = os.path.join ('orders_by_customer_name', where_letter + '.json')
        self.write_orders_json(orders_json, outpath)

    def write_orders_json (self, data_json, path):
        fp = open (path, 'w')
        fp.write (json.dumps(data_json, sort_keys=False, indent=4, separators=(',', ': ')))
        fp.close()
        print 'json written to {}'.format(path)


if __name__ == '__main__':
    writer = OrderByCustomerWriter()
    where_clause = "UPPER(lastname) LIKE 'A%'"
    # where_clause = "customerid = '10168'"   # a lot of orders

    if 0: # sanity check
        customers = writer.get_customers(where_clause)
        print '{} customers found'.format(len(customers))

    if 0:  # small sample
        json_data = writer.get_orders_json(where_clause)
        # print json.dumps(json_data, indent=3)
        writer.write_orders_json(json_data, 'ORDERS_BY_CUSTOMER.json')

    writer.write_orders_batch_json (where_clause)
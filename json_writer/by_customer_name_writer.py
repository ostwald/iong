import sys, os, re, time, json, datetime

sys.path.append ('/Users/ostwald/devel/projects/')
sys.path.append ('/Users/ostwald/devel/')

from iong import schemas
sys.path.append (schemas.python_lib_dir)


from iong import OrdersTable, OrderDetailsTable, CustomersTable
from iong import utils

"""
select * from customers where UPPER(lastname) < 'A' ORDER BY lastname, firstname ASC

select * from customers where UPPER(lastname) LIKE 'A%' ORDER BY UPPER(lastname), UPPER(firstname) ASC
"""

class OrderByCustomerWriter:

    order_by = None   # e.g., "UPPER(lastname), UPPER(firstname)"
    data_dir_name = None   # e.g., 'customer_name'

    def __init__ (self):
        self.orders_table = OrdersTable()
        self.customers_table = CustomersTable()
        self.order_details_table = OrderDetailsTable()
        self.orders_json = None

    def get_orders_json (self, where_clause):

        customers =  self.customers_table.get_customers(where=where_clause, order_by=self.order_by)

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

    def get_where_clause (self, where_letter):
        num = ord(where_letter.upper())
        if num < ord('A'):
            return "UPPER(lastname) < 'A'"
        else:
            return "UPPER(lastname) LIKE '{}%'".format(chr(num))

    def write_orders_batch_json (self, where_letter):
        """
        start is of form YYYY-MM-DD
        """
        print '\nwhere_letter: {}'.format(where_letter)
        # pat = re.compile ("UPPER\(lastname\) LIKE \'([A-Z])\%\'")
        # m = pat.match (where_clause)
        # if not m:
        #     raise Exception ('Could not parse where clause: ({})'.format(where_clause))
        # where_letter = m.group(1)

        where_clause = self.get_where_clause (where_letter)
        if where_letter == '@':
            where_letter = 'other'
        outpath = os.path.join (schemas.json_data_dir, self.data_dir_name, where_letter + '.json')

        # print '{} -- {}'.format(where_clause, outpath)

        orders_json = self.get_orders_json(where_clause)
        self.write_orders_json(orders_json, outpath)

    def write_orders_json (self, data_json, path):
        if not os.path.exists (os.path.dirname(path)):
            os.makedirs (os.path.dirname(path))
        fp = open (path, 'w')
        fp.write (json.dumps(data_json, sort_keys=False, indent=4, separators=(',', ': ')))
        fp.close()
        print 'json written to {}'.format(path)

class OrderByCustomerNameWriter (OrderByCustomerWriter):
    order_by = "UPPER(lastname), UPPER(firstname)"
    data_dir_name = 'customer_name'

if __name__ == '__main__':
    writer = OrderByCustomerWriter()
    where_clause = "UPPER(lastname) LIKE 'C%'"
    # where_clause = "customerid = '10168'"   # a lot of orders

    if 0: # sanity check
        customers = writer.get_customers(where_clause)
        print '{} customers found'.format(len(customers))

    if 0:  # small sample

        where_clause = "UPPER(lastname) LIKE 'C%'"
        json_data = writer.get_orders_json(where_clause)
        # print json.dumps(json_data, indent=3)

        if 1:
            # send to default path (data)
            outpath = os.path.join (schemas.json_data_dir,  'customer_name', 'C.json')
            writer.write_orders_json(json_data, outpath)
        if 0:

            outpath = os.path.join (schemas.json_sandbox, 'ORDERS_BY_CUSTOMER.json')
            writer.write_orders_json(json_data, outpath)

    if 0:
        for i in range (ord('A')-1, ord('Z')+1):
            where_letter = chr(i)
            writer.write_orders_batch_json (where_letter)
import sys, os, re, time, json, datetime

sys.path.append ('/Users/ostwald/devel/projects/')
sys.path.append ('/Users/ostwald/devel/')

from iong import schemas
sys.path.append (schemas.python_lib_dir)

from by_customer_name_writer import OrderByCustomerWriter
from iong import utils

class OrderByCustomerEmailWriter (OrderByCustomerWriter):

    data_dir_name = 'customer_email'
    order_by = "UPPER(emailaddress)"

if __name__ == '__main__':
    writer = OrderByCustomerEmailWriter()
    LETTER = 'B'
    where_clause = "UPPER(emailaddress) LIKE '{}%'".format(LETTER)
    # where_clause = "customerid = '10168'"   # a lot of orders

    if 0: # sanity check
        customers = writer.get_customers(where_clause)
        print '{} customers found'.format(len(customers))

    if 0:  # small sample

        json_data = writer.get_orders_json(where_clause)
        # print json.dumps(json_data, indent=3)

        if 1:
            # send to default path (data)
            outpath = os.path.join (schemas.json_data_dir,  writer.data_dir_name, '{}.json'.format(LETTER))
            writer.write_orders_json(json_data, outpath)
        if 0:

            outpath = os.path.join (schemas.json_sandbox, 'ORDERS_BY_CUSTOMER_EMAIL.json')
            writer.write_orders_json(json_data, outpath)

    if 1:
        for i in range (ord('A')-1, ord('Z')+1):
            where_letter = chr(i)
            writer.write_orders_batch_json (where_letter)
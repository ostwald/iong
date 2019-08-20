import sys, os, re
import schemas

sys.path.append (os.path.dirname(schemas.ion_devel_dir))

# for EXISTINBG
from customers_table import CustomersTable
from orders_table import OrdersTable

# for new
from ion_db_ingest import DBTable

class CustomerAllTable(CustomersTable):
    table_name = 'customers_all'


orders_table = OrdersTable()
customer_ids = orders_table.get_customer_ids()
# print customer_ids

print 'inserting records for {} into new customer table'.format(len(customer_ids))

customer_all_table = CustomerAllTable()

customer_table = DBTable(schemas.sqlite_file, 'customers', schemas.customer)

for id in customer_ids:
    print id
    rec = customer_all_table.get_customer(id)
    if rec.data is not None:
        customer_table.add_record(rec)



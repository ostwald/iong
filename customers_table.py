import sys, os, re, time, json

sys.path.append ('/Users/ostwald/devel/python-lib/')


from ion_table import DBTable, DBRecord
from order_details_table import OrderDetailsTable
import schemas

class CustomerRecord(DBRecord):
    schema_fields = schemas.customer

class CustomersTable (DBTable):

    sqlite_file = schemas.sqlite_file
    schema_fields = schemas.customer
    # sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
    # sqlite_file = '/Users/ostwald/devel/projects/iong/ion_db.sqlite'
    table_name = 'customers'

    def get_customer (self, customerid):
        query = "SELECT *  FROM `{tn}` WHERE customerid = '{id}'" \
            .format(tn=self.table_name, id=customerid)

        self.cursor.execute(query)
        row = self.cursor.fetchone()

        return CustomerRecord(row)


def get_customer_tester():
    table = CustomersTable()

    customer = table.get_customer('29620')

    for field in customer.schema:
        print '- {} : {}'.format(field, customer[field])

    print json.dumps(customer.asDict())

if __name__ == '__main__':
    get_customer_tester()
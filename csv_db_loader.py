"""
Load a CSV file into an sqlite database
"""

import sys, os, re, time

sys.path.append ('/Users/ostwald/devel/python-lib/')

from tabdelimited import CsvFile, FieldList, CsvRecord

import sqlite3
from ion_db_ingest import DBTable

class CSVLoader:


    def __init__(self, csv_path, sqlite_file, table_name):
        self.sqlite_file = sqlite_file
        self.table_name = table_name
        self.csv_reader = CsvFile ()
        self.csv_reader.linesep = '\r'
        self.csv_reader.read(csv_path)
        print '%d records read' % len(self.csv_reader)

        self.db_table = DBTable (self.sqlite_file, self.table_name, self.make_db_schema_spec())

    def load_table(self):

        for row in self.csv_reader:
            self.db_table.add_record (row)

        print 'Database Loaded'


    def make_db_schema_spec (self):
        schema_spec = []
        for field in self.csv_reader.schema:
            schema_spec.append([field, 'TEXT', lambda x:x[field]])

        return schema_spec


if __name__ == '__main__':
    sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'

    if 0:
        table_name = 'orders'
        path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/since_2016/Orders.csv'
        # path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/test/Orders.csv'
        # path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/test/Orders-tiny.csv'

    if 0:
        table_name = 'order_details'
        path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/since_2016/OrderDetails.csv'

    if 1:
        table_name = 'customers'
        path = '/Users/ostwald/Documents/ION_DB/data/IONG_Orders/select_fields/Customers_selected_fields.csv'

    loader = CSVLoader(path, sqlite_file, table_name)
    loader.load_table()
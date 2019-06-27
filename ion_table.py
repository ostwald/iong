import sys, os, re, time, string

sys.path.append ('/Users/ostwald/devel/python-lib')

from tabdelimited import FieldList, CsvRecord

from jloFS import JloFile
from UserDict import UserDict
from UserList import UserList

import sqlite3

def get_time_str(secs):
    date_time_fmt = '%Y-%m-%d %H:%M:%S'
    return time.strftime(date_time_fmt, time.localtime(secs))

def get_checksum(path):
    m = hashlib.new('md5')
    m.update (open (path, 'r').read())
    return m.hexdigest()

class DBRecord:
    """
    A record consisting of a list of data values, and a schema that provides
    field names and accessors to the data
    """

    def __init__(self, data, schema):
        """
        data - a list of values
        parent - an object that has a 'schema' attribute
        """
        self.data = data
        self.schema = schema

    def __getitem__(self, field):
        """
        Provides field-based addressing so that values can be obtained by field name.
        Returns the empty string if the field is not found in the schema
        """
        index = self.schema.getIndex(field)
        return self.data[index]

    def __repr__ (self):
        """
        Returns a formatted string representation of this entry
        """

        return self.asTabDelimitedRecord().join (", ")

    def asTabDelimitedRecord (self):
        """
        joins the fields of this record as a list in schema order.
        E.g., used too write the AddressBook to disk
        """
        fields = [];add=fields.append
        for field in self.schema:
            add (self[field])
        return string.join (fields, '\t')

class DBTable:

    schema_fields = []
    sqlite_file = ''
    table_name = ''

    def __init__(self):
        self.schema = self.make_schema()
        conn = sqlite3.connect(self.sqlite_file)
        self.cursor = conn.cursor()

    def make_schema(self):
        return FieldList(self.schema_fields)



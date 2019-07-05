import sys, os, re, time
from jloFS import JloFile
from UserDict import UserDict
from UserList import UserList

import sqlite3

class Schema_Field:

    def __init__ (self, data):
        self.name = data[0]
        self.type = data[1]

    def get_value(self, obj):
        # if type(self.value_fn) in [type(0), type(''), type (0.5)]:
        #     return self.value_fn
        # else:
        #     return self.value_fn(obj)
        return obj[self.name]

class Schema (UserDict):

    def __init__ (self, spec):
        self.data = {}
        self.fields = UserList()
        self.field_order = UserList()
        for item in spec:
            field = Schema_Field(item)
            self.data[field.name] = field
            self.fields.append(field)
            self.field_order.append(field.name)
        self.quoted_schema = self._get_quoted_schema()

    def get_index (self, field):
        return self.field_order.index(field)

    def _get_quoted_schema(self):
        return ','.join(map (lambda x:"'%s'" % x, self.field_order))

    def obj_to_data_values(self, obj):
        row_value_list = []
        for field in self.fields:
            val = field.get_value(obj)
            if type(val) == type('') or type(val) == type(u''):
                try:
                    row_value_list.append(u"'{}'".format(val.replace ("'", "%27")))
                except UnicodeEncodeError, msg:
                    print msg
                    print "val: %s" % val
                    # row_value_list.append (u"")
                    sys.exit(1)

            if type(val) == type(1) or type(val) == type(1.5):
                row_value_list.append(unicode(val))
        quoted_values = u','.join(row_value_list)

        return quoted_values

def get_time_str(secs):
    date_time_fmt = '%Y-%m-%d %H:%M:%S'
    return time.strftime(date_time_fmt, time.localtime(secs))

def get_checksum(path):
    m = hashlib.new('md5')
    m.update (open (path, 'r').read())
    return m.hexdigest()

class DBTable:


    def __init__(self, sqlite_file, table_name, schema_spec=None):
        self.sqlite_file = sqlite_file
        self.table_name = table_name
        self.schema_spec = schema_spec
        self.schema = self.make_schema()
        if not self.table_exists():
            self.setup()

    def table_exists (self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{tn}';" \
                  .format(tn=self.table_name))
        tables = c.fetchall()
        conn.close()
        return len(tables)

    def make_schema(self):
        return Schema(self.schema_spec)

    def setup(self):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # apparently we need at least one field to create a record
        first_field = self.schema.fields[0]
        c.execute('CREATE TABLE {tn} ({fn} {ft})' \
                  .format(tn=self.table_name, fn=first_field.name, ft=first_field.type))

        if len(self.schema.fields)  > 1:
            for field in self.schema.fields[1:]:
                c.execute("ALTER TABLE {tn}  ADD COLUMN '{cn}' {ct}" \
                          .format(tn=self.table_name, cn=field.name, ct=field.type))

        conn.commit()
        conn.close()

    def add_record (self,row):
        conn = sqlite3.connect(self.sqlite_file)
        c = conn.cursor()

        # quoted_schema = ','.join(map (lambda x:"'%s'" % x, HOSTS_SCHEMA_SPEC))
        quoted_schema = self.schema.quoted_schema

        # put data list together to match with schema fields
        quoted_values = self.schema.obj_to_data_values(row)

        try:
            c.execute(u"INSERT INTO {tn} ({fn}) VALUES ({fv})" \
                      .format(tn=self.table_name, fn=quoted_schema, fv=quoted_values))
        except:
            print('ERROR: {}'.format(sys.exc_info()))
            print 'quoted_schema: %s' % quoted_schema
            print 'quoted_values: %s' % type(quoted_values)
            sys.exit(1)

        conn.commit()
        conn.close()


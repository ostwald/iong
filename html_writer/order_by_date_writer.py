import os, sys, re, json
from UserDict import UserDict
from UserList import UserList

sys.path.append ('/Users/ostwald/devel/python/python-lib/')
sys.path.append ('/Users/ostwald/devel/')

from html import HtmlDocument
from HyperText.HTML40 import *


class Address:
    def __init__ (self, data, prefix):
        self.data = data
        self.prefix = prefix

        for key in self.data.keys():
            if key.startswith(prefix):
                attr = key[len(prefix):]
                setattr (self, attr, self.data[key])
                print '{}: {}'.format(attr, getattr(self, attr))

    def asHtml(self):
        d = DIV (klass="{}_address".format(self.prefix))
        if len(self.companyname) > 0:
            d.append (DIV (self.companyname, klass='companyname'))
        d.append (DIV ('{} {}'.format(self.firstname, self.lastname)))
        d.append (DIV(self.address1))
        if len(self.address2) > 0:
            d.append (DIV(self.address2))

        d.append (DIV ('{}, {} {}'.format(self.city, self.state, self.postalcode)))

        d.append (DIV (self.phonenumber, klass="phonenumber"))

        return d

class Detail:

    def __init__ (self, data):
        self.data = data

    def asHtml (self):
        d = DIV (klass='order_details')
        title = '{} x {} ({})'.format(self.data['quantity'], self.data['productname'], self.data['productcode'])
        d.append(DIV (title))
        d.append (DIV (self.data['optionids'], klass='optionids'))
        return d

class OrderEntry (UserDict):

    def __init__ (self, data):
        self.data = data
        self.order = data['order']
        self.billing_address = Address (self.order, 'billing')
        self.ship_address = Address (self.order, 'ship')
        self.customer = data['customer']
        self.details = map (Detail, data['details'])
        
    def asHtml (self):
        html = DIV(klass='order_entry')
        addresses = DIV (klass='order_addresses')
        addresses.append (self.billing_address.asHtml())
        addresses.append (self.ship_address.asHtml())
        html.append(addresses)

        for detail in self.details:
            html.append (detail.asHtml())

        return html


if __name__ == '__main__':
    json_data_path = '/Users/ostwald/devel/projects/iong/json_writer/ORDERS_BY_DATE.json'
    orders = map (OrderEntry, json.loads(open(json_data_path, 'r').read()))
    print '{} orders read'.format(len(orders))


    if 1:
        order_entry = orders[0]
        print order_entry.asHtml().__str__()


    # <link rel='stylesheet' type='text/css' href='styles.css'>
    stylesheet = "styles.css"

    # <script language="JavaScript" src="javascript.js" />
    javascript = "javascript.js"


    doc = HtmlDocument (stylesheet=stylesheet, javascript=javascript)

    for entry in orders:
        doc.body.append(entry.asHtml())


    print doc

    #
    # # shipping = Address (order_entry.order, 'ship')
    # shipping = Address (order_entry.order, 'billing')
    # print shipping.asHtml().__str__()
    #
    # detail = order_entry.details[0]
    # print detail.asHtml()
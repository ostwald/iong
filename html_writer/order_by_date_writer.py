import os, sys, re, json, codecs
from UserDict import UserDict
from UserList import UserList

sys.path.append ('/Users/ostwald/devel/python/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects')

from html import HtmlDocument
from HyperText.HTML40 import *

from iong import utils


class Address:
    def __init__ (self, data, prefix):
        self.data = data
        self.prefix = prefix

        for key in self.data.keys():
            if key.startswith(prefix):
                attr = key[len(prefix):]
                setattr (self, attr, self.data[key])
                # print '{}: {}'.format(attr, getattr(self, attr))

    def asHtml(self):
        d = DIV (klass="{}_address".format(self.prefix))
        if len(self.companyname) > 0:
            d.append (DIV (self.companyname, klass='companyname'))
        d.append (DIV (u'{} {}'.format(self.firstname, self.lastname)))
        d.append (DIV(self.address1))
        if len(self.address2) > 0:
            d.append (DIV(self.address2))

        d.append (DIV (u'{}, {} {}'.format(self.city, self.state, self.postalcode)))

        d.append (DIV (self.phonenumber, klass="phonenumber"))

        return d

class Detail:

    def __init__ (self, data):
        self.data = data

    def asHtml (self):
        d = DIV (klass='order_details')
        title = u'{} x {} ({})'.format(self.data['quantity'], self.data['productname'], self.data['productcode'])
        d.append(DIV (title))
        # d.append (DIV (self.data['optionids'], klass='optionids'))
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
        html = LI(klass='order', id=self.order['orderid'])
        addresses = DIV (klass='order_addresses')
        addresses.append (self.billing_address.asHtml())
        addresses.append (self.ship_address.asHtml())
        html.append(addresses)

        for detail in self.details:
            html.append (detail.asHtml())

        return html

class OrderByDateDocument (HtmlDocument):


    home = '/Users/ostwald/devel/projects/iong/html_writer/html'

    DOCTYPE = Markup ("doctype","html")

    def write (self, filename=None):
        if filename is None:
            filename = 'orderByDate_TESTER'
        path = os.path.join (self.home, filename + '.html')
        self.writeto (path)
        print 'written to {}'.format(path)

    def writeto(self, path, indent=0, perlevel=2):
        f = codecs.open (path, 'w', 'utf8')
        f.write (self.__str__())
        f.close()


def get_order_day (order):
    return order['orderdate'].split(' ')[0].strip()

if __name__ == '__main__':
    json_data_path = '/Users/ostwald/devel/projects/iong/json_writer/orders_per_month/2016-01-03.json'
    orders = map (OrderEntry, json.loads(open(json_data_path, 'r').read()))
    print '{} orders read'.format(len(orders))


    if 0:
        order_entry = orders[0]
        print order_entry.asHtml().__str__()


    # <link rel='stylesheet' type='text/css' href='styles.css'>
    stylesheet = "styles.css"

    # <script language="JavaScript" src="javascript.js" />
    javascript = ["https://ajax.googleapis.com/ajax/libs/jquery/1.12.1/jquery.min.js",
                  "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
                  "moment.min.js",
                  "base-script.js",
                  "javascript.js"
                  ]

    doc = OrderByDateDocument (stylesheet=stylesheet, javascript=javascript)

    order_list = DIV(id='orders')


    current_day = get_order_day(orders[0])
    current_order_list = UL(klass="order-list")
    for entry in orders:
        order_day = get_order_day(entry)

        if order_day != current_day:
            order_list_item = LI ()
            order_list_item.append(DIV (current_day,  id=utils.get_iso_day(current_day), klass="order-date-header"))
            order_list_item.append (current_order_list)
            order_list.append(order_list_item)

            current_day = order_day
            current_order_list = UL(klass="order-list")

        current_order_list.append(entry.asHtml())


    doc.body.append(order_list)

    # print unicode (doc.__str__())
    doc.write()

    #
    # # shipping = Address (order_entry.order, 'ship')
    # shipping = Address (order_entry.order, 'billing')
    # print shipping.asHtml().__str__()
    #
    # detail = order_entry.details[0]
    # print detail.asHtml()
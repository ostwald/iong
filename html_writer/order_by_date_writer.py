import os, sys, re, json, codecs
from UserDict import UserDict
from UserList import UserList

sys.path.append ('/Users/ostwald/devel/python/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects')

from html import HtmlDocument
from HyperText.HTML40 import *
from iong import utils, schemas


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
        # d.append (DIV ("{} address".format(self.prefix), klass='address_label'))
        if len(self.companyname) > 0:
            d.append (DIV (self.companyname, klass='companyname'))
        d.append (DIV (u'{} {}'.format(self.firstname, self.lastname)))
        d.append (DIV(self.address1))
        if len(self.address2) > 0:
            d.append (DIV(self.address2))

        d.append (DIV (u'{}, {} {}'.format(self.city, self.state, self.postalcode)))

        return d

    def normalize_phonenumber(self):
        s = list(self.phonenumber)
        if len(s) == 10:
            s.insert(3,'-')
            s.insert(7,'-')
            return ''.join(s)
        return self.phonenumber

class SchemaObj:

    schema = None

    def __init__ (self, data):
        self.data = data
        for field in self.schema:
            setattr (self, field, self.data[field])


class Detail(SchemaObj):

    schema = schemas.order_details

    def asHtml (self):
        d = DIV (klass='order_details')
        title = u'{} x {} ({})'.format(self.quantity, self.productname, self.productcode)
        d.append(DIV (title))
        # d.append (DIV (self.optionids, klass='optionids'))
        return d

class Customer(SchemaObj):

    schema = schemas.customer

    def asHtml(self):
        try:
            title = u''
            if self.companyname:
                title = u'{} '.format(self.companyname)
            title += u'{} {}  ({})'.format(self.firstname, self.lastname, self.emailaddress)
            return  DIV (title, klass='customer')
        except:
            print 'Could not render customer: {}'.format(sys.exc_info()[1])
            return DIV (klass='customer')


class OrderEntry (UserDict):

    def __init__ (self, data):
        self.data = data
        self.order = data['order']
        self.billing_address = Address (self.order, 'billing')
        self.ship_address = Address (self.order, 'ship')
        self.customer = Customer(data['customer'])
        self.details = map (Detail, data['details'])
        
    def render (self, parent):
        header = H3 (utils.get_human_date(self.order['orderdate']))
        order_wrapper = DIV(klass='order', id=self.order['orderid'])
        cust_html = self.customer.asHtml()

        parent.append(header)
        parent.append(order_wrapper)

        header.append(cust_html)
        order_wrapper.append(self.make_addresses_table())

        for detail in self.details:
            order_wrapper.append (detail.asHtml())

    def make_addresses_table (self):
        table = TABLE(klass='adresses-table')
        table.append( TR (
            TH ('billing address'), TH ('ship address')
        ))
        table.append (TR(
            TD(self.billing_address.asHtml()),
            TD(self.ship_address.asHtml()),
        ))
        table.append (TR(
            TD(self.billing_address.normalize_phonenumber(), klass='phonenumber'),
            TD(self.ship_address.normalize_phonenumber(), klass='phonenumber'),
        ))
        return table


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
    json_data_path = '/Users/ostwald/devel/projects/iong/json_writer/ORDERS_BY_DATE.json'
    orders = map (OrderEntry, json.loads(open(json_data_path, 'r').read()))
    print '{} orders read'.format(len(orders))


    if 0:
        order_entry = orders[0]
        print order_entry.asHtml().__str__()


    # <link rel='stylesheet' type='text/css' href='styles.css'>
    stylesheet = [
        "//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css",
        "styles.css"
    ]

    # <script language="JavaScript" src="javascript.js" />
    javascript = [
        "//code.jquery.com/jquery-1.12.4.js",
        "//code.jquery.com/ui/1.12.1/jquery-ui.js",
        # "https://ajax.googleapis.com/ajax/libs/jquery/1.12.1/jquery.min.js",
        # "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
        "moment.min.js",
        "base-script.js",
        "javascript.js"
    ]

    doc = OrderByDateDocument (stylesheet=stylesheet, javascript=javascript)

    order_list = DIV(id='orders')

    current_day = get_order_day(orders[0])
    current_order_list = DIV(klass="order-list")

    for entry in orders:
        order_day = get_order_day(entry)

        if order_day != current_day:
            order_header = H2(utils.get_human_date(current_day),id=current_day, klass="order-date-header")
            order_list.append(order_header)

            # order_list.append(H2 (utils.get_human_date(current_day),
            #                            id=current_day, klass="order-date-header"))

            # order_list_item.append(DIV (utils.get_human_date(current_day),  id=current_day, klass="order-date-header"))
            order_list.append (current_order_list)

            current_day = order_day
            current_order_list = DIV(klass="order-list")

        entry.render (current_order_list)


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
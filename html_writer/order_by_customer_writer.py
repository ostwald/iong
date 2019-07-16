import os, sys, re, json, codecs
from UserDict import UserDict
from UserList import UserList

sys.path.append ('/Users/ostwald/devel/python/python-lib/')
sys.path.append ('/Users/ostwald/devel/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects')
sys.path.append ('/Users/ostwald/devel')

from html import HtmlDocument
from HyperText.HTML40 import *
from iong import utils, schemas

from writer_models import Address, Customer, Detail, IongHtmlDocument

class CustomerOrderHtmlDoc (IongHtmlDocument):
    javascript_defaults = [
        "//code.jquery.com/jquery-1.12.4.js",
        "//code.jquery.com/ui/1.12.1/jquery-ui.js",
        "../moment.min.js",
        "../base-script.js",
        "../customers-script.js"
    ]

    stylesheet_defaults = [
        "//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css",
        "../styles.css",
        "../customers-styles.css"
    ]

    html_root = os.path.join (schemas.ion_devel_dir, 'html_writer/html')
    data_dir = os.path.join (schemas.ion_devel_dir, 'json_writer/orders_by_customer_name')
    html_output_dir = os.path.join (html_root, 'lastname')

    def __init__ (self, *content, **attrs):
        if not attrs.has_key("index_letter"):
            raise Exception, "index_letter is a required param"
        self.index_letter = attrs['index_letter'].upper()
        self.filename = self.index_letter == '@' and 'other' or self.index_letter

        del(attrs['index_letter'])
        IongHtmlDocument.__init__ (self, *content, **attrs)

        print 'index letter is {}'.format(self.index_letter)

    def render_navbar (self):
        navbar = TABLE (id='navbar')
        for i in range (ord('A')-1, ord('Z')+1):
            if i == ord('A')-1:
                name = "other"
            else:
                name = chr(i)

            if chr(i) == self.index_letter:
                cell = TD (name, klass="navcell current_cell")
            else:
                # href = os.path.join (self.html_root, 'lastname', name+'.html')
                cell = TD (Href(name+'.html', name), klass="navcell")

            # cell['klass'] = "CELL"
            navbar.append (cell)

        self.body.append(navbar)

    def render (self):
        json_data_path = os.path.join (schemas.ion_devel_dir, 'json_writer/orders_by_customer_name','{}.json'.format(self.filename))

        entries = map (CustomerEntry, json.loads(open(json_data_path, 'r').read()))
        print '{} entries read'.format(len(entries))


        # doc = CustomerOrderHtmlDoc (index_letter=letter)

        # navbar = DIV (id="navbar")
        # navbar.append (DIV ("prev", klass='prev-button'))
        # navbar.append (DIV ("next", klass='next-button'))

        self.render_navbar()

        self.body.append (H1 ('Orders grouped by Customer Name'))

        entry_list = DIV(id='customers')

        for entry in entries:
            entry.render(entry_list)


        self.body.append(entry_list)

    def write (self):
        path = os.path.join (self.html_output_dir, self.filename+'.html')
        self.writeto (path)
        print 'written to {}'.format(path)


class CustomerEntry (UserDict):
    def __init__ (self, data):
        self.data = data
        self.customer = Customer(self.data['customer'])
        self.orders = self.data['orders']

    def render (self, parent):
        # header = H2 (self.customer.asHtml().content[0], klass='customer-header')
        self.render_header(parent)

        # parent.append(header)
        order_list = DIV(klass="order-list")
        parent.append(order_list)
        for order_entry in map (OrderEntry, self.orders):
            order_entry.render(order_list)

    def render_header(self, parent):

        name_str = u'{}, {}'.format(self.customer.lastname, self.customer.firstname)
        name = SPAN (name_str, klass='customer-name')
        if len (self.customer.companyname) > 0:
            c_str = u' ({})'.format(self.customer.companyname)
            company = SPAN (c_str, klass='company-name')
        else:
            company = None

        email = SPAN (self.customer.emailaddress, klass='customer-email')
        id = SPAN('customer #'+self.customer.customerid, klass='customer-id')

        # c_str += ' {}   customer #{}'.format (emailaddress, self.customer.customerid)

        num_orders = DIV(str(len(self.orders)), ' orders', klass="num-orders")

        header = H2 (name, klass='customer-header')
        header.append (num_orders)
        if company:
            header.append (company)
        header.append (email)
        header.append (id)
        parent.append (header)

class OrderEntry (UserDict):

    def __init__ (self, data):
        self.data = data
        self.order = data['order']
        self.billing_address = Address (self.order, 'billing')
        self.ship_address = Address (self.order, 'ship')
        # self.customer = Customer(data['customer'])
        self.details = map (Detail, data['details'])

    def render (self, parent):
        # headerStr = '{}    order #{}'.format(utils.get_human_date(self.order['orderdate']), self.order['orderid'])
        headerStr = utils.get_human_date(self.order['orderdate'])

        order_num = SPAN('Order #{}'.format(self.order['orderid']), klass="order_num")
        header = H3 (headerStr)
        header.append (order_num)

        order_wrapper = DIV(klass='order', id=self.order['orderid'])
        # cust_html = self.customer.asHtml()

        parent.append(header)
        parent.append(order_wrapper)

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

def main (letter, outpath='orderByCustomer_TESTER'):

    doc = CustomerOrderHtmlDoc (index_letter=letter)
    doc.render()
    doc.write()

class CustomerOrderIndexDoc(CustomerOrderHtmlDoc):

    def __init__ (self, *content, **attrs):
        IongHtmlDocument.__init__ (self, *content, **attrs)
        self.filename = 'index'
        self.index_letter = None

    def render(self):
        self.render_navbar()
        self.body.append (H1 ('Orders grouped by Customer Name'))


def render_index_page():
    doc = CustomerOrderIndexDoc ()
    doc.render()
    doc.write()

def render_all ():
    for i in range (ord('A')-1, ord('Z')+1):
        main(chr(i))


if __name__ == '__main__':

    # raw = """[What is Your Desired Delivery Date?:Deliver ASAP (Be sure to select the correct method of shipping at check out)][Message:ENTER YOUR GIFT MESSAGE HERE INCLUDING SIGNATURE][Leaves:Lake Champlain Chocolate Leaves (O,AG)][Brie cheese and hot pepper rasp:Brie Cheese and Hot Pepper Raspberry Spread (N,G,AG)][ Adult Coloring Kit:The Mindfulness Coloring Book and Pen Set Anti-Stress Kit][ Eye Mask Warmie:Intelex Heatable Lavender Eye Mask][Tea Superfruit:Republic of Tea Superfruit Green Tea Assortment - 24 bags (N,G)][ Clif choco pistachios:Clif Family Kitchen Dark Chocolate Toffee Pistachios (N,AG)][Blueberries and chocolate:Bissinger%27s Dark Chocolate Covered Blueberries (G,N,AG)][ Enjoy Life Mountain Mambo Mix:Enjoy Life Seed and Fruit Mix (G,N,V,K)][Apple Mango Chips:Fruitivity Crunchy Mango Apple Chips (N,G,NGMO,C)][Caramel Popcorn:Rocky Mountain Caramel Popcorn (N,G,AG,C)][White Cheddar Popcorn:Rocky Mountain White Cheddar Popcorn (N,G,AG,C)][34 Degrees Sesame Crackers:34 Degrees Sesame Crackers (N,A,C)][Martinellis:Martinelli%27s Organic Sparkling Cider (O,G,K)][Body oil:Aura Cacia Relaxing Lavender Aromatherapy Massage/Body Oil][Candle Illuminature:Illuminature Glass Candle (N,AG,C)]"""
    # print str(parse_options(raw))

    if 0:   # write one html doc
        letter = 'C'
        main(letter)

    if 0:
        render_all()

    render_index_page()



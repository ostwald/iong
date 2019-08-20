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
from customer_writer_models import CustomerOrderHtmlDoc, CustomerEntry



class CustomerNameEntry (CustomerEntry):

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

class CustomerNameOrderHtmlDoc (CustomerOrderHtmlDoc):
    json_data_dir = os.path.join (schemas.json_data_dir,'customer_name')
    html_output_dir = os.path.join (schemas.html_root_dir, 'customer_name')
    entry_class = CustomerNameEntry
    page_title = 'Orders grouped by Customer Name'

def main (letter, outpath='orderByCustomer_TESTER'):

    doc = CustomerNameOrderHtmlDoc (index_letter=letter)
    doc.render()
    doc.write()

class CustomerNameOrderIndexDoc(CustomerOrderHtmlDoc):

    html_output_dir = os.path.join (schemas.html_root_dir, 'customer_name')

    def __init__ (self, *content, **attrs):
        IongHtmlDocument.__init__ (self, *content, **attrs)
        self.filename = 'index'
        self.index_letter = None

    def render(self):
        self.render_navbar()
        self.body.append (H1 ('Orders grouped by Customer Name'))


def render_index_page():
    doc = CustomerNameOrderIndexDoc ()
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

    if 1:
        render_all()

    render_index_page()



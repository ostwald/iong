import os, sys, re, json, codecs
from UserDict import UserDict
from UserList import UserList

sys.path.append ('/Users/ostwald/devel/python/python-lib/')
sys.path.append ('/Users/ostwald/devel/projects')
sys.path.append ('/Users/ostwald/devel')

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
    options_pat = re.compile( '\[([^\]]*)\]')

    def asHtml (self):
        d = DIV (klass='order_details')
        title = u'{} x {} ({})'.format(self.quantity, self.productname, self.productcode)
        d.append(DIV (utils.unescape(title)))
        d.append (DIV (self.parse_options(), klass='options'))
        return d

    def parse_options (self):
        raw = utils.unescape(self.options)
        m = self.options_pat.findall (raw)
        order_list = UL (klass='detail-options')
        for item in m:
            order_list.append (LI (item.strip()))
        return order_list

class Customer(SchemaObj):

    schema = schemas.customer

    def asHtml(self):
        try:
            title = u''
            if self.companyname:
                title = u'{} '.format(self.companyname)
            title += u'{} {}  ({})  #{}'.format(self.firstname, self.lastname, self.emailaddress, self.customerid)
            return  DIV (title, klass='customer')
        except:
            print 'Could not render customer: {}'.format(sys.exc_info()[1])
            return DIV (klass='customer')

class IongHtmlDocument (HtmlDocument):

    # home = '/Users/ostwald/devel/projects/iong/html_writer/html'
    home = os.path.join(schemas.ion_devel_dir, 'html_writer/html')

    DOCTYPE = Markup ("doctype","html")

    # <link rel='stylesheet' type='text/css' href='styles.css'>
    stylesheet_defaults = [
        "//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css",
        "styles.css"
    ]

    # <script language="JavaScript" src="javascript.js" />
    javascript_defaults = [
        "//code.jquery.com/jquery-1.12.4.js",
        "//code.jquery.com/ui/1.12.1/jquery-ui.js",
        # "https://ajax.googleapis.com/ajax/libs/jquery/1.12.1/jquery.min.js",
        # "https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
        "moment.min.js",
        "base-script.js",
        "javascript.js"
    ]

    def __init__ (self, *content, **attrs):
        attrs['stylesheet'] = self.stylesheet_defaults
        attrs['javascript'] = self.javascript_defaults
        HtmlDocument.__init__ (self, *content, **attrs)


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


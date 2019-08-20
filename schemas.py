import os

## home
ion_devel_dir = '/Users/ostwald/devel/iong'
sqlite_file = os.path.join (ion_devel_dir, 'ion_db.sqlite')
# sqlite_file = '/Users/ostwald/devel/iong/ion_db.sqlite'

python_lib_dir = os.path.join (os.path.dirname(ion_devel_dir), 'python-lib')

# python_lib_dir = '/Users/ostwald/devel/'
# json_sandbox = 'json_writer/data/sandbox'
json_data_dir = os.path.join (ion_devel_dir, 'json_writer/data')
json_sandbox = os.path.join (json_data_dir, 'sandbox')

html_root_dir = os.path.join (ion_devel_dir, 'html_writer/html')
html_data_dir = os.path.join (ion_devel_dir, 'html_writer/html/data')
html_sandbox = os.path.join (ion_devel_dir, 'html_writer/html/sandbox')

## work
# sqlite_file = '/Users/ostwald/devel/projects/iong/ion_db.sqlite'
# ion_devel_dir = '/Users/ostwald/devel/projects/iong'


order_details = [
    'orderdetailid',
    'orderid',
    'productcode',
    'productname',
    'quantity',
    'optionids',
    'options',
]

order = [
    'orderid',
    'customerid',
    'billingcompanyname',
    'billingfirstname',
    'billinglastname',
    'billingaddress1',
    'billingaddress2',
    'billingcity',
    'billingstate',
    'billingpostalcode',
    'billingcountry',
    'billingphonenumber',
    'shipcompanyname',
    'shipfirstname',
    'shiplastname',
    'shipaddress1',
    'shipaddress2',
    'shipcity',
    'shipstate',
    'shippostalcode',
    'shipcountry',
    'shipphonenumber',
    'paymentamount',
    'orderdate',
]

customer = [
    'customerid',
    'firstname',
    'lastname',
    'companyname',
    'emailaddress',
]
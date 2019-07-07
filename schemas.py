# sqlite_file = '/Users/ostwald/Documents/ION_DB/ion_db.sqlite'
sqlite_file = '/Users/ostwald/devel/projects/iong/ion_db.sqlite'


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
    'orderdate',
]

customer = [
    'customerid',
    'firstname',
    'lastname',
    'companyname',
    'emailaddress',
]
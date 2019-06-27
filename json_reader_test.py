import sys, os, json
from orders_table import OrderRecord

content = open('JSON_TESTER.json', 'r').read()
orders = json.loads(content)

print '{} orders read'.format(len(orders))

instances = map (OrderRecord, orders)

print 'instances instantiated'
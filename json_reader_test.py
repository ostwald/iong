import sys, os, json
from orders_table import OrderRecord

content = open('JSON_orders_TESTER.json', 'r').read()
orders_map = json.loads(content)

print '{} orders read'.format(len(orders_map))

instances = []
for key in orders_map.keys():
    instances.append (OrderRecord (orders_map[key]))


print '{} instances instantiated'.format(len(instances))

for i, order in enumerate(instances):
    print order
    break
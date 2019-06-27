import sys, os, json

content = open('JSON_TESTER.json', 'r').read()
orders = json.loads(content)

print '{} orders read'.format(len(orders))
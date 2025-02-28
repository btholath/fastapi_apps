import time
from pprint import pprint

from main import redis, Product

key = 'order-completed'
group = 'warehouse-group'

try:
  redis.xgroup_create(name=key, groupname=group, mkstream=True)
  print("Group created")
except Exception as e:
  print(str(e))

while True:
  try:
    results = redis.xreadgroup(groupname=group, consumername=key, streams={key: '>'})
    print(results)
    if results != []:
      for result in results:
        print("--------result----------")
        pprint(result)
        print(f"Order Status = {results[0][0]}")
        print(f"Product Id = {results[0][1][0][1]['product_id']}")
        print(f"quantity = {results[0][1][0][1]['quantity']}")
        obj = results[0][1][0][1]
        try:
          print(f"product_id={Product.get(obj['product_id'])}  quantity={int(obj['quantity'])}")
          product = Product.get(obj['product_id'])
          product.quantity -= int(obj['quantity'])
          product.save()
          print(product)
        except:
          redis.xadd(name='refund-order', fields=obj)
  except Exception as e:
    print(str(e))
  time.sleep(3)
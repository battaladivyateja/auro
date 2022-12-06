import xmltodict
import pprint
  
with open('orders.xml','r') as file:
    xml_orders = file.read()
Order_book = xmltodict.parse(xml_orders)
pprint.pprint(order_book, indent=2)
# for i in Order_book:
#     print(i)

import xml.etree.ElementTree as ET
import time
import sys
import os
import argparse
from collections import OrderedDict

# created the class OrderBook

class OrderBook:
    def __init__(self, book):
        self.book = book
        self.buy = OrderedDict()
        self.sell = OrderedDict()

    def __str__(self):
        return "Buy {0}\nSell {1}".format(self.buy, self.sell)
#function for adding the orders
    def adding_order(self, each_order):
        if each_order.operation == "BUY":
            self.adding_buy_order(each_order)
        elif each_order.operation == "SELL":
            self.add_sell_order(each_order)

# function for adding the bought orders
    def adding_buy_order(self, each_order):
        if each_order.price in self.buy:
            self.buy[each_order.price].append(each_order)
        else:
            self.buy[each_order.price] = [each_order]

#function for adding the selling orders.
    def adding_selling_order(self, each_order):
        if each_order.price in self.sell:
            self.sell[each_order.price].append(each_order)
        else:
            self.sell[each_order.price] = [each_order]

#function for deleting the orders.
    def deleting_order(self, each_order):
        if each_order.operation == "BUY":
            self.deleting_buy_order(each_order)
        elif order.operation == "SELL":
            self.deleting_sell_order(each_order)

#function for deleting the bought orders.
    def deleting_buy_order(self, each_order):
        if each_order.price in self.buy:
            for i, o in enumerate(self.buy[each_order.price]):
                if o.orderId == each_order.orderId:
                    del self.buy[each_order.price][i]
                    break

#function for deleting the selling orders.
    def deleting_sell_order(self, each_order):
        if each_order.price in self.sell:
            for i, o in enumerate(self.sell[each_order.price]):
                if o.orderId == each_order.orderId:
                    del self.sell[each_order.price][i]
                    break

#function for matching the orders.
    def matching(self, each_order):
        if each_order.operation == "BUY":
            self.match_buy(each_order)
        elif each_order.operation == "SELL":
            self.match_sell(each_order)

#matching of the buying of the books
    def match_buy(self, each_order):
        for price, orders in self.sell.items():
            if price <= each_order.price:
                for o in orders:
                    if o.volume > each_order.volume:
                        o.volume -= each_order.volume
                        each_order.volume = 0
                        break
                    else:
                        each_order.volume -= o.volume
                        o.volume = 0
                if each_order.volume == 0:
                    break

#matching of the selling books.
    def match_sell(self, each_order):
        for price, each_orders in self.buy.items():
            if price >= each_order.price:
                for o in each_orders:
                    if o.volume > each_order.volume:
                        o.volume -= each_order.volume
                        each_order.volume = 0
                        break
                    else:
                        each_order.volume -= o.volume
                        o.volume = 0
                if each_order.volume == 0:
                    break

#initializing the orders of the books
class Orders:
    def __init__(self, operation, bk, pr, vol, order_id):
        self.operation = operation
        self.book = bk
        self.price = pr
        self.volume = vol
        self.orderId = order_id

    def __str__(self):
        return "{0} {1} {2} {3} {4}".format(self.operation, self.book, self.price, self.volume, self.orderId)


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root


def parse_order(each_order):
    operation = each_order.get("operation")
    bk = each_order.get("books")

    if each_order.get("price") is None:
        pr = 0
    else:
        pr = float(each_order.get("price"))
    if each_order.get("volume") is None:
        vol = 0
    else:
        vol = each_order.get("volume")
    order_id = each_order.get("orderId")
    return Orders(operation, bk, pr, vol, order_id)

#processing the orders of the books.
def order_processing(each_order, books_order):
    
    #if the book f the book does not exist, we creates it.
    if each_order.book not in books_order:
        books_order[each_order.book] = OrderBook(each_order.book)
    
    #opeartion of adding the order.
    
    if each_order.operation == "ADD":
        books_order[each_order.book].adding_order(each_order)
   
    #operation of deleting the order.
    elif each_order.operation == "DEL":
        books_order[each_order.book].deleting_order(each_order)
    
    #operation of matching the order
    elif each_order.operation == "MATCH":
        books_order[each_order.book].matching(each_order)


if __name__ == "__main__":
    #reading the given orders file
    order_xml = parse_xml("orders.xml")
    
    #created a dictionary of books.
    books_order = {}
    #processing of the each order record in the file.
    for each_order in order_xml:
        order_processing(parse_order(each_order), books_order)

    #printing of the books after processing.
    for each_book, books_order in books_order.items():
        print(each_order)
        print(books_order)


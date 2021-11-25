from dataclasses import dataclass
from typing import List
import csv

class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    def __repr__(self):
        prod_repr_str = "- - - - - - - - - - - - - -\n"
        prod_repr_str += f"PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}\n"
        prod_repr_str += "- - - - - - - - - - - - - \n"
        return prod_repr_str

class ProductStock:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def name(self):
        return self.product.name

    def price(self):
        return self.product.price

    def cost(self):
        return self.price * self.quantity

    def __repr__(self):
        return f"{self.product} PRODUCT QUANTITY: {self.quantity}"

class Shop:

    def __init__(self, csv_path):
        self.stock = []
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            cash = next(csv_reader)[0] #shop's cash is stored in first row so using next() to grab first line from csv_reader
            self.cash = float(cash) #set shop's cash, cast as float so not a string
            for row in csv_reader:
                product = Product(name=row[0], price=float(row[1])) #set product details, enforce float type for price
                product_stock = ProductStock(product=product,quantity=int(row[2])) #set product stock details, enforce type of int for quantity
                self.stock.append(product_stock) #append product_stock to shop's stock list

    def __repr__(self):
        shop_repr_str = "\n|||-----=====SHOP DETAILS=====-----|||\n\n"
        shop_repr_str += f'Shop balance - {self.cash:.2f}\n'
        for i in self.stock:
            shop_repr_str += f"{i.product}\n"
            shop_repr_str += f"The shop has {i.quantity} of the above\n"
        shop_repr_str += "\n|||-----=====SHOP DETAILS=====-----|||\n\n"
        return shop_repr_str
    

class Customer:

    def __init__(self, csv_path=None):
        self.shopping_list = []
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            first_row = next(csv_reader) #customer's name and budget is stored in first row so using next() to grab first line from csv_reader
            self.name = first_row[0]
            self.budget = float(first_row[1]) #set customer's cash
            for row in csv_reader:
                product = Product(name=row[0], price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
                product_quantity = ProductStock(product=product,quantity=int(row[1])) #set ProductStock item, to be appended to customers shopping list
                customer.shopping_list.append(product_quantity) #append product_quantity to customer's shopping list

    def __repr__(self):
        shop_repr_str = "\n|||-----=====Customer  DETAILS=====-----|||\n\n"
        shop_repr_str += f'Shop balance - {self.cash:.2f}\n'
        for i in self.stock:
            shop_repr_str += f"{i.product}\n"
            shop_repr_str += f"The shop has {i.quantity} of the above\n"
        shop_repr_str += "\n|||-----=====SHOP DETAILS=====-----|||\n\n"
        return shop_repr_str
'''
prod_test = Product(name="Bread", price=1.1)
print(prod_test)
stock_test = ProductStock(product=prod_test, quantity=10)
print(stock_test)
'''

shop_test = Shop(csv_path='Shop Stock\\stock.csv')

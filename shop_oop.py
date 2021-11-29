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

    def fulfill_order(self, cust):
        print("FULFILL_ORDER")

    def shop_interface(self):
        selection = ''
        while selection != "0":
            selection = input("\nPlease choose an option:\n(1) Normal customer order\n(2) Customer order with not enough money\n(3) Customer order with excess quantity\n(4) Live Order\n(5) Check shop stock and balance\n(0) Exit Shop\n")
            if selection == "1":
                customer = Customer('Customer Orders\\customer_order_a.csv')
                self.fulfill_order(customer)
            elif selection == "2":
                customer = Customer('Customer Orders\\customer_order_b.csv')
                self.fulfill_order(customer)
            elif selection == "3":
                customer = Customer('Customer Orders\\customer_order_c.csv')
                self.fulfill_order(customer)
            elif selection == "4":
                print("LIVE ORDER Come back later")
                customer = Customer().create_live_mode()
                self.fulfill_order(customer)
            elif selection == "5":
                print(self)

    def __repr__(self):
        shop_repr_str = "\n|||-----=====SHOP DETAILS=====-----|||\n"
        shop_repr_str += f'Shop balance - {self.cash:.2f}\n'
        for i in self.stock:
            shop_repr_str += f"{i.product}"
            shop_repr_str += f"The shop has {i.quantity} of the above\n\n"
        shop_repr_str += "|||-----=====SHOP DETAILS=====-----|||\n\n"
        return shop_repr_str


class Customer:

    def __init__(self, csv_path=None):
        #if no csv_path provided, give default values, expect create_live_mode function to later be called
        if csv_path is None:
            self.shopping_list = []
            self.name = ''
            self.budget = 0
        #else load in csv and create customer variables
        else:
            self.shopping_list = []
            with open(csv_path, "r") as csv_file:
                csv_reader = csv.reader(csv_file,delimiter=',')
                first_row = next(csv_reader) #customer's name and budget is stored in first row so using next() to grab first line from csv_reader
                self.name = first_row[0]
                self.budget = float(first_row[1]) #set customer's cash
                for row in csv_reader:
                    product = Product(name=row[0], price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
                    product_quantity = ProductStock(product=product,quantity=int(row[1])) #set ProductStock item, to be appended to customers shopping list
                    self.shopping_list.append(product_quantity) #append product_quantity to customer's shopping list

    def create_live_mode(self):
        self.shopping_list = []
        cust_name = str(input("Please enter your name: "))
        self.name = cust_name
        cust_budget = float(input("Please enter your budget: "))
        self.budget = cust_budget
        product_name = str(input("\nEnter name of product or 0 to stop \n"))
        while(product_name != "0"):
            quantity = int(input(f"Enter quantity of {product_name} to order \n"))
            product = Product(name=product_name, price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
            product_quantity = ProductStock(product=product,quantity=quantity) #set ProductStock item to be appended to customers shopping list
            self.shopping_list.append(product_quantity) #append product_stock to shop's stock list
            product_name = str(input("\nEnter name of product or 0 to stop \n"))

    def __repr__(self):
        cust_repr_str = f"\n|||-----=====CUSTOMER {self.name} ORDER DETAILS=====-----|||\n\n"
        cust_repr_str += f'Customer budget - {self.budget:.2f}\n'
        for i in self.shopping_list:
            cust_repr_str += f"{i.product}"
            cust_repr_str += f"Customer wants {i.quantity} of the above\n\n"
        cust_repr_str += f"\n|||-----=====CUSTOMER {self.name} ORDER DETAILS=====-----|||\n\n"
        return cust_repr_str
'''
prod_test = Product(name="Bread", price=1.1)
print(prod_test)
stock_test = ProductStock(product=prod_test, quantity=10)
print(stock_test)
'''

shop_test = Shop(csv_path='Shop Stock\\stock.csv')
cust_test = Customer(csv_path='Customer Orders\\customer_order_a.csv')
print(cust_test)

cust_test2 = Customer()
#cust_test2.create_live_mode()
#print(cust_test2)

shop_test.shop_interface()
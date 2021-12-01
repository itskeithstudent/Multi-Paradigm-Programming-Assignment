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

    def find_price(self, product_name):
        for i in self.stock:
            if i.product.name == product_name:
                product_price = i.product.price
                return product_price
        #in-case nothing found
        print("Product not found in shop stock, please check for any typos and try again.")
        product_price = 0 #product_price set to 0 if not found, rather than removing item from shopping list
        return product_price

    def check_stock(self, product_name, product_quantity):
        #loop through items in shop stock
        for i in self.stock:
            if product_name == i.product.name:
                print(f"Checking shop stock of {i.product.name}, quantity in stock - {i.quantity}")
                if i.quantity >= product_quantity:
                    return product_quantity
                else:
                    print(f"Updating quantity to match what shop has in stock - {i.quantity}")
                    return i.quantity
        #if have gone through entire shop stock and no match, then shop doesn't stock item, return 0 for this item
        print("We don't stock this item.")
        return 0

    def update_shop(self, product_name, quantity_removed):
        for i in self.stock:
            if i.product.name == product_name:
                i.quantity = i.quantity - quantity_removed

    def fulfill_order(self, cust):
        order_total = 0.0
        cust_budget = cust.budget
        print("___________________________________________________________________")
        print(f"Hello {cust.name}, I'll now start processing your order!")
        print("===================================================================\n")
        for i in cust.shopping_list:
            price = self.find_price(i.product.name)
            #checked_quantity stores the quantity returned from check_stock, which is either the original quantity requested (if in-stock) or whatever stock the shop has
            checked_quantity = self.check_stock(i.product.name,i.quantity)
            print(f"Customer has requested {i.quantity} of {i.product.name}, actual quantity that can be provided {checked_quantity}\n")
            i.quantity = checked_quantity
            #order_total will be what is subtracted from customer budget and added to shop cash
            order_total = order_total + (price * checked_quantity)
        if order_total > cust_budget:
            print("===================================================================")
            print("You don't have enough money, my apologies, please revise your order and try again.")
            print("___________________________________________________________________")
        else:
            #Now Loop back through customer order and update the shop inventory as order is determined to be fulfillable
            print("===================================================================")
            print(f"Thank you for your custom, that will be {order_total:.2f} total please.")
            print("___________________________________________________________________")
            #loop through customer shopping_list, update shop stock quantities
            for i in cust.shopping_list:
                self.update_shop(i.product.name,i.quantity)
            #add order_total to shop's cash
            self.cash += order_total
            #remove order_total from customers budget
            cust.budget -= order_total

    def shop_interface(self):
        selection = ''
        #command line menu for interacting with shop
        while selection != "0":
            selection = input("\nPlease choose an option:\n(1) Normal customer order\n(2) Customer order with not enough money\n(3) Customer order with excess quantity\n(4) Live Order\n(5) Check shop stock and balance\n(0) Exit Shop\n")
            if selection == "1":
                customer = Customer('..\\Customer Orders\\customer_order_a.csv')
                self.fulfill_order(customer)
            elif selection == "2":
                customer = Customer('..\\Customer Orders\\customer_order_b.csv')
                self.fulfill_order(customer)
            elif selection == "3":
                customer = Customer('..\\Customer Orders\\customer_order_c.csv')
                self.fulfill_order(customer)
            elif selection == "4":
                customer = Customer()
                customer.create_live_mode()
                self.fulfill_order(customer)
            elif selection == "5":
                #takes advantage of shop class __repr__ function to show shop details
                print(self)
        #print exit shop message
        print("Bye have a wonderful time!")

    def __repr__(self):
        shop_repr_str = "\n|||-----=====SHOP DETAILS=====-----|||\n"
        shop_repr_str += f'Shop balance - {self.cash:.2f}\n'
        for i in self.stock:
            shop_repr_str += f"{i.product}"
            shop_repr_str += f"The shop has {i.quantity} of the above\n\n"
        shop_repr_str += "|||-----=====SHOP DETAILS=====-----|||\n"
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
        print(cust_budget)
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

shop = Shop(csv_path='..\\Shop Stock\\stock.csv')

shop.shop_interface()


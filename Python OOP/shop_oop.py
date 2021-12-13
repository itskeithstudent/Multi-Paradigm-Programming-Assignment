from dataclasses import dataclass
from typing import List
import csv

class Product:
    '''
    Creates object for holding product details, name of product and its price

    Attributes:
        name : str
        price : float

    Function:
        N/A
    '''
    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    def __repr__(self):
        prod_repr_str = "- - - - - - - - - - - - - -\n"
        prod_repr_str += f"PRODUCT NAME: {self.name}\nPRODUCT PRICE: {self.price}\n"
        prod_repr_str += "- - - - - - - - - - - - - \n"
        return prod_repr_str

class ProductStock:
    '''
    Creates object for holding stock of a product details, name of product and its price

    Attributes:
        product : class Product
        quantity : int

    Function:
        name - returns name of the Product object
        price - returns price of the Product object
        cost - returns price of the Product object multiplied by the quantity attribute
    '''
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
    '''
    Creates a object for holding shop details and allows customer interaction, which updates state of object.

    Attributes:
        stock : list
        cash : float

    Functions:
        find_price - get's price of a product if finds its name retruns price, otherwise returns 0
        check_stock - checks if requested quantity can be met, if it can returns requested quantity, otherwise returns max quantity in stock
        update_stock - updates quantity of product in shop stock, returns nothing but will change quantity value in shop stock item
        fulfill_order - fulfill's a customer order, taking in a customer object and checking if their requested products and quantities can be 
            met and whether they have enough budget to pay for the order, if so then shop's product stock quantities get updated and shop's cash
            increases.
        shop_interface - presents command line interface for interacting with shop, selecting different types of order including a live mode, 
            and a print out of current state of shop
    '''

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
        '''
        find_price - checks self for a product and returns the price of it if it has that product in stock
        parameters:
        product_name (string) - name of the product to be checked
        returns:
        price of the requested product
        '''
        for i in self.stock:
            if i.name() == product_name:
                product_price = i.price()
                return product_price
        #in-case nothing found
        print("Product not found in shop stock, please check for any typos and try again.")
        product_price = 0 #product_price set to 0 if not found, rather than removing item from shopping list
        return product_price

    def check_stock(self, product_name, product_quantity):
        '''
        check_stock - checks self for a product and the quantity it has in stock of that product
        parameters:
        product_name (string) - name of the product to be checked
        product_quantity (int) - quantity of the product being sought
        returns:
        requested quantity if self has enough stock
        maximum quantity in self if it doesn't have enough stock
        0 otherwise
        '''
        #loop through items in shop stock
        for i in self.stock:
            if product_name == i.name():
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
        '''
        update_shop - updates the quantity of a product in self
        parameters:
        product_name (string) - name of the product who's quantity is to be updated
        quantity_removed (int) - quantity of the product being updated in shop
        returns:
        N/A, shop is updated in-place
        '''
        for i in self.stock:
            if i.name() == product_name:
                i.quantity = i.quantity - quantity_removed

    def fulfill_order(self, cust):
        '''
        fulfill_order - fullfills customer order against self, adjusts customer order depending on self stock
            customer order success depends on their budget being >= to the order price
        parameters:
        cust (class Customer) - customer object looking to place an order
        returns:
        N/A, self is updated but nothing returned
        '''
        order_total = 0.0
        cust_budget = cust.budget
        print("___________________________________________________________________")
        print(f"Hello {cust.name}, I'll now start processing your order!")
        print("===================================================================\n")
        for i in cust.shopping_list:
            price = self.find_price(i.name())
            #checked_quantity stores the quantity returned from check_stock, which is either the original quantity requested (if in-stock) or whatever stock the shop has
            checked_quantity = self.check_stock(i.name(),i.quantity)
            print(f"Customer has requested {i.quantity} of {i.name()}, actual quantity that can be provided {checked_quantity}\n")
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
                self.update_shop(i.name(),i.quantity)
            #add order_total to shop's cash
            self.cash += order_total
            #remove order_total from customers budget
            cust.budget -= order_total

    def shop_interface(self):
        '''
        shop_interface - displays the options for interacting with the shop (e.g. self)
        takes in no parameters and returns nothing, but calls funtions depending on input which change state of shop (self)
        '''
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
        shop_repr_str = "\n|||-----=====SHOP DETAILS=====-----|||\n\n"
        shop_repr_str += f'Shop balance - {self.cash:.2f}\n\n'
        for i in self.stock:
            shop_repr_str += f"{i.product}"
            shop_repr_str += f"The shop has {i.quantity} of the above\n"
        shop_repr_str += "\n|||-----=====SHOP DETAILS=====-----|||\n"
        return shop_repr_str


class Customer:
    '''
    Creates a object for holding customer details to order against a shop object with.

    Attributes:
        shopping_list : list
        name: str
        budget: float

    Functions:
        create_live_mode - generate a series of prompts to get customer details from command line terminal instead of csv file,
            returns nothing as updaets Customer class attributes
    '''
    def __init__(self, csv_path=None):
        '''
        __init__ takes in optional argument for csv_path, if nothing supplied, created blank customer object, expect to use create_live_mode function
            to update details, otherwise it get's a csv file which it reads for customer details.
        '''
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
        '''
        create_live_mode - populates self attributes, assumes no csv loaded in at initializing this class, however will work regardless
        parameters:
        N/A - operates on self
        returns:
        N/A - updates state of the object, so doesn't need to return anything
        '''
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


if __name__ == '__main__':
    #load in shop
    shop = Shop(csv_path='..\\Shop Stock\\stock.csv')
    #start interacting with shop
    shop.shop_interface()
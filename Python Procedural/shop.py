from dataclasses import dataclass
from typing import List
import csv

# DataClass for a product
@dataclass
class Product:
    name:str
    price:float

# DataClass for amount of product in Stock
@dataclass
class ProductStock:
    product:Product
    quantity:int

# DataClass for shop, stores shop's cash and a list of items in stock
@dataclass
class Shop:
    cash:float
    stock:List[ProductStock]

# DataClass for customer, similar to shop but takes a name, budget instead of cash and a shopping list (same as shop stock, but won't hold price)
@dataclass
class Customer:
    name:str
    budget:float
    shopping_list:List[ProductStock]

def printProduct(p):
    '''
        printProduct - prints name and price of a product dataclass
        parameters:
        p (dataclass) - product dataclass
        returns:
        N/A, just prints details from the product dataclass
    '''
    print("- - - - - - - - - - - - - -")
    print(f"PRODUCT NAME: {p.name}\nPRODUCT PRICE: {p.price}")
    print("- - - - - - - - - - - - - ")

def printShop(s):
    '''
        printShop - prints details for items in a shop
        parameters:
        s (dataclass) - shop dataclass
        returns:
        N/A, just prints details from the shop dataclass.
        Calls on printProduct function for each product in stock.
    '''
    print("\n|||-----=====SHOP DETAILS=====-----|||\n")
    print(f"Shop balance - {s.cash:.2f}\n")
    for i in s.stock:
        printProduct(i.product)
        print(f"The shop has {i.quantity} of the above\n")
    print("|||-----=====SHOP DETAILS=====-----|||\n")

def createAndStockShop(shop_csv):
    '''
        createAndStockShop - creates a shop dataclass, taking input from a csv
        parameters:
        shop_csv (string) - file path to csv representing shop
        returns:
        shop dataclass after populating data
    '''
    shop = Shop(cash=0,stock=[]) #Initialise Shop dataclass with default values, for cash and stock

    with open(shop_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        cash = next(csv_reader)[0] #shop's cash is stored in first row so using next() to grab first line from csv_reader
        shop.cash = float(cash) #set shop's cash, cast as float so not a string
        for row in csv_reader:
            product = Product(name=row[0], price=float(row[1])) #set product details, enforce float type for price
            product_stock = ProductStock(product=product,quantity=int(row[2])) #set product stock details, enforce type of int for quantity
            shop.stock.append(product_stock) #append product_stock to shop's stock list
    return shop

def createCustomerOrder(customer_csv):
    '''
        createCustomerOrder - creates a customer dataclass, taking input from a csv
        parameters:
        customer_csv (string) - file path to csv representing a customer
        returns:
        customer dataclass after populating data
    '''
    customer = Customer(name="",budget=0,shopping_list=[]) #Initialise Shop dataclass with default values, for cash and stock

    with open(customer_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        first_row = next(csv_reader) #customer's name and budget is stored in first row so using next() to grab first line from csv_reader
        customer.name = first_row[0]
        customer.budget = float(first_row[1]) #set customer's cash
        for row in csv_reader:
            product = Product(name=row[0], price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
            product_quantity = ProductStock(product=product,quantity=int(row[1])) #set ProductStock item, to be appended to customers shopping list
            customer.shopping_list.append(product_quantity) #append product_quantity to customer's shopping list
    return customer

def createLiveCustomerOrder():
    '''
        createLiveCustomerOrder - creates a customer dataclass, takes no input arguments, instead inputs from command line
        parameters:
        N/A
        returns:
        customer dataclass after populating data
    '''
    cust = Customer(name="",budget=0,shopping_list=[]) #Initialise Shop dataclass with default values, for cash and stock
    cust_name = str(input("Please enter your name: "))
    cust.name = cust_name
    cust_budget = float(input("Please enter your budget: "))
    cust.budget = cust_budget

    product_name = str(input("\nEnter name of product or 0 to stop \n"))
    while(product_name != "0"):
        quantity = int(input(f"Enter quantity of {product_name} to order \n"))
        product = Product(name=product_name, price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
        product_quantity = ProductStock(product=product,quantity=quantity) #set ProductStock item to be appended to customers shopping list
        cust.shopping_list.append(product_quantity) #append product_stock to shop's stock list
        product_name = str(input("\nEnter name of product or 0 to stop \n"))

    return cust

def check_stock(shop, product_name, product_quantity):
    '''
        check_stock - checks a shop dataclass for a product and the quantity it has in stock of that product
        parameters:
        shop (dataclass) - dataclass for the shop to have its stock checked
        product_name (string) - name of the product to be checked
        product_quantity (int) - quantity of the product being sought
        returns:
        requested quantity if shop has enough stock
        maximum quantity in the shop if it doesn't have enough stock
        0 otherwise
    '''
    #loop through items in shop stock
    for i in shop.stock:
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

def find_price(shop, product_name):
    '''
        find_price - checks a shop dataclass for a product and returns the price of it if it has that product in stock
        parameters:
        shop (dataclass) - dataclass for the shop to have its stock checked
        product_name (string) - name of the product to be checked
        returns:
        price of the requested product
    '''
    for i in shop.stock:
        if i.product.name == product_name:
            product_price = i.product.price
            return product_price
    #in-case nothing found
    print("Product not found in shop stock, please check for any typos and try again.")
    product_price = 0 #product_price set to 0 if not found, rather than removing item from shopping list
    return product_price

def update_shop(shop, product_name, quantity_removed):
    '''
        update_shop - updates the quantity of a product in a shop dataclass in-place
        parameters:
        shop (dataclass) - dataclass for the shop to have its stock updated
        product_name (string) - name of the product who's quantity is to be updated
        quantity_removed (int) - quantity of the product being updated in shop
        returns:
        N/A, shop is updated in-place
    '''
    for i in shop.stock:
        if i.product.name == product_name:
            i.quantity = i.quantity - quantity_removed

def fulfill_order(shop, cust):
    '''
        fulfill_order - fullfills customer order against shop, adjusts customer order depending on shop stock
            customer order success depends on their budget being >= to the order price
        parameters:
        shop (dataclass) - dataclass for the shop to fulfill order against
        cust (dataclass) - dataclass for the customer looking to place an order
        returns:
        N/A, shop is updated in-place, customer is also updated in-place (though only it's budget)
    '''
    order_total = 0.0
    cust_budget = cust.budget
    print("\n___________________________________________________________________")
    print(f"Hello {cust.name}, I'll now start processing your order!")
    print("===================================================================\n")
    for i in cust.shopping_list:
        price = find_price(shop, i.product.name)
        #checked_quantity stores the quantity returned from check_stock, which is either the original quantity requested (if in-stock) or whatever stock the shop has
        checked_quantity = check_stock(shop,i.product.name,i.quantity)
        print(f"Customer has requested {i.quantity} of {i.product.name}, actual quantity that can be provided {checked_quantity}\n")
        i.quantity = checked_quantity
        #order_total will be what is subtracted from customer budget and added to shop cash
        order_total = order_total + (price * checked_quantity)
    if order_total > cust_budget:
        print("\n===================================================================")
        print("You don't have enough money, my apologies, please revise your order and try again.")
        print("___________________________________________________________________\n")
    else:
        #Now Loop back through customer order and update the shop inventory as order is determined to be fulfillable
        print("\n===================================================================")
        print(f"Thank you for your custom, that will be {order_total:.2f} total please.")
        print("___________________________________________________________________\n")
        #loop through customer shopping_list, update shop stock quantities
        for i in cust.shopping_list:
            update_shop(shop,i.product.name,i.quantity)
        #add order_total to shop's cash
        shop.cash += order_total
        #remove order_total from customers budget
        cust.budget -= order_total

if __name__ == '__main__':
    #set up shop variable to start
    shop = createAndStockShop('..\\Shop Stock\\stock.csv')
    selection = ''
    #take in inputs from user in command line to interact with shop
    while selection != "0":
        selection = input("\nPlease choose an option:\n(1) Normal customer order\n(2) Customer order with not enough money\n(3) Customer order with excess quantity\n(4) Live Order\n(5) Check shop stock and balance\n(0) Exit Shop\n")
        if selection == "1":
            customer = createCustomerOrder('..\\Customer Orders\\customer_order_a.csv')
            fulfill_order(shop,customer)
        elif selection == "2":
            customer = createCustomerOrder('..\\Customer Orders\\customer_order_b.csv')
            fulfill_order(shop,customer)
        elif selection == "3":
            customer = createCustomerOrder('..\\Customer Orders\\customer_order_c.csv')
            fulfill_order(shop,customer)
        elif selection == "4":
            customer = createLiveCustomerOrder()
            fulfill_order(shop,customer)
        elif selection == "5":
            printShop(shop)
    #print exit message after entering "0"
    print("Bye have a wonderful time!")
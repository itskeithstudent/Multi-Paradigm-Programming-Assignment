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

@dataclass
class Shop:
    cash:float
    stock:List[ProductStock]

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
    print("- - - - - - - - - - - - - -\n")
    print(f"PRODUCT NAME: {p.name}\nPRODUCT PRICE: {p.price}\n")
    print("- - - - - - - - - - - - - \n")

def printShop(s):
    '''
        printShop - prints details for items in a shop
        parameters:
        s (dataclass) - shop dataclass
        returns:
        N/A, just prints details from the shop dataclass.
        Calls on printProduct function for each product in stock.
    '''
    print("\n|||-----=====SHOP DETAILS=====-----|||\n\n")
    print(f"Shop balance - {s.cash:.2f}\n")
    for i in s.stock:
        printProduct(i.product)
        print(f"The shop has {i.quantity} of the above\n")
    print("\n|||-----=====SHOP DETAILS=====-----|||\n\n")

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
        #budget = float(next(csv_reader)[0])
        first_row = next(csv_reader) #customer's name and budget is stored in first row so using next() to grab first line from csv_reader
        customer.name = first_row[0]
        customer.budget = float(first_row[1]) #set shop's cash
        for row in csv_reader:
            product = Product(name=row[0], price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
            product_quantity = ProductStock(product=product,quantity=int(row[1])) #set ProductStock item to be appended to customers shopping list
            customer.shopping_list.append(product_quantity) #append product_stock to shop's stock list
    return customer

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
            print(f"Checking shop stock of {i.product.name}, quantity in stock - {i.quantity}\n")
            if i.quantity >= product_quantity:
                return product_quantity
            else:
                print(f"Updating quantity to match what shop has in stock - {i.quantity}\n")
                return i.quantity
    #if have gone through entire shop stock and no match, then shop doesn't stock item, return 0 for this item
    print("We don't stock this item.")
    return 0

def findPrice(shop, product_name):
    '''
        findPrice - checks a shop dataclass for a product and returns the price of it if it has that product in stock
        parameters:
        shop (dataclass) - dataclass for the shop to have its stock checked
        product_name (string) - name of the product to be checked
        returns:
        price of the requested product
    '''
    for i in shop.stock:
        if i.product.name == product_name:
            product_price = i.product.price
            print(product_price)
            return product_price
    #in-case nothing found
    print("Product not found in shop stock, please check for any typos and try again.")

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

if __name__ == '__main__':
    shop = createAndStockShop('Shop Stock\\stock.csv')
    printShop(shop)
    customer = createCustomerOrder('Customer Orders\\customer_order_a.csv')
    
    #findPrice(shop, "Coke Can")
    #check_stock(shop, "Coke Can", 1000)
    #update_shop(shop, "Coke Can", 100)
    #printShop(shop)
    # print("\nPlease choose an option:\n(1) Normal customer order\n(2) Customer order with not enough money\n(3) Customer order with excess quantity\n(4) Live Order\n(5) Check shop stock and balance\n(0) Exit Shop\n")
    # selection = ''
    # while selection != "0":
    #     selection = input()
    #     if selection == "1":
    #         print("Normal order")
    #     elif selection == "2":
    #         print("no Normal order")
    #     elif selection == "3":
    #         print("no Normal order")
    #     elif selection == "4":
    #         print("no Normal order")
    #     elif selection == "5":
    #         print("no Normal order")

    # print("Bye have a wonderful time!")
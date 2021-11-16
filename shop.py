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

def createAndStockShop(shop_csv):
    shop = Shop(cash=0,stock=[]) #Initialise Shop dataclass with default values, for cash and stock

    with open(shop_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        cash = next(csv_reader)[0] #shop's cash is stored in first row so using next() to grab first line from csv_reader
        shop.cash = cash #set shop's cash
        for row in csv_reader:
            product = Product(name=row[0], price=row[1]) #set product details
            product_stock = ProductStock(product=product,quantity=row[2]) #set product stock details
            shop.stock.append(product_stock) #append product_stock to shop's stock list
    return shop

def createCustomerOrder(customer_csv):
    customer = Customer(name="",budget=0,shopping_list=[]) #Initialise Shop dataclass with default values, for cash and stock

    with open(customer_csv, "r") as csv_file:
        csv_reader = csv.reader(csv_file,delimiter=',')
        budget = next(csv_reader)[0] #customer's budget is stored in first row so using next() to grab first line from csv_reader
        customer.budget = budget #set shop's cash
        for row in csv_reader:
            product = Product(name=row[0], price=0.0) #set product details, customer doesn't know items price so leaving as 0.0 (inflation is very high these days, hard to keep track of price of things!)
            product_quantity = ProductStock(product=product,quantity=row[1]) #set ProductStock item to be appended to customers shopping list
            customer.shopping_list.append(product_quantity) #append product_stock to shop's stock list
    return customer

if __name__ == '__main__':
    shop = createAndStockShop('Shop Stock\\stock.csv')
    customer = createCustomerOrder('Customer Orders\\customer_order_a.csv')
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
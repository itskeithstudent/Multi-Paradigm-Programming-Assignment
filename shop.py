from dataclasses import dataclass
from typing import List

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
    shoppingList:List[ProductStock]

if __name__ == '__main__':
    
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
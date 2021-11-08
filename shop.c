#include <stdio.h>
#include <string.h>
#include <stdlib.h>
//Struct for a product e.g. struct Product irn_bru = {"Bottle Bru", 2.5};
struct Product
{
    char *name;
    double price;
};

//Struct for amount of product in Stock
struct ProductStock
{
    struct Product product;
    int quantity;
};

struct Shop
{
    double cash;
    struct ProductStock stock[20];
    int index;
};

struct Customer
{
    char *name;
    double budget;
    struct ProductStock shoppingList[10];
    int index;
};

void printProduct(struct Product p)
{
    printf("- - - - - - - - - - - - - -\n");
    printf("PRODUCT NAME: %s \nPRODUCT PRICE: %.2f \n", p.name, p.price);
    printf(" - - - - - - - - - - - - - \n");
};

void printCustomer(struct Customer c)
{
    printf("- - - - - - - - - - - - - -\n");
    printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f \n", c.name, c.budget);
    printf(" - - - - - - - - - - - - - \n");
    //in below for loop had to add index to customer struct to keep track of
    for (int i = 0; i < c.index; i++)
    {
        printProduct(c.shoppingList[i].product);
        printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
        double cost = c.shoppingList[i].product.price * c.shoppingList[i].quantity;
        printf("The cost to %s will be %.2f\n", c.name, cost);
    };
}

struct Customer createCustomerOrder(char *file_loc)
{

    //printf(file_loc);
    //printf("See me");
    struct Customer cust;
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    size_t read;
    //fp=fopen(file_loc,"r");
    fp = fopen(file_loc, "r");
    if (fp == NULL)
    {
        printf("file not found!");
        exit(EXIT_FAILURE);
    }

    //get the first line of csv file, should be single numeric value representing shop's balance
    getline(&line, &len, fp);

    //get customer name from first line of csv
    char *cn = strtok(line, ",");
    char *cust_name = malloc(sizeof(char) * 50);
    strcpy(cust_name, cn); //copy value from pointer into allocated memory
    cust.name = cust_name; //set struct name

    //get customer budget from first line of csv after first comma
    char *t = strtok(NULL, ",");
    double total = atof(t); //convert string to double
    cust.budget = total;

    printf("Name from file %s \n", cust_name);
    printf("Budget from file %.2f \n", total);

    printf("Budget(cash) from cust struct %.2f\n", cust.budget);

    while ((read = getline(&line, &len, fp)) != -1)
    {
        //printf("%s - is line\n", line);
        //printf(line);
        // printf(len);
        char *n = strtok(line, ",");
        char *q = strtok(NULL, ",");
        char *name = malloc(sizeof(char) * 50);
        strcpy(name, n);
        int quantity = atoi(q);

        //struct Product product = {name,price};
        struct Product productDetail = {name, 0.0};
        struct ProductStock stockItem = {productDetail, quantity};
        cust.shoppingList[cust.index++] = stockItem;
        printf("STRUCT NAME OF PRODUCT %s QUANT %.2f\n", stockItem.product.name, stockItem.product.price);
        printf("NAME OF PRODUCT %s QUANT %d\n", name, quantity);
    };
    return cust;
}

struct Shop createAndStockShop()
{
    struct Shop shop = {200};
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    size_t read;
    //printf("YOO");
    fp = fopen("Shop Stock\\stock.csv", "r");
    if (fp == NULL)
    {
        printf("file not found");
        exit(EXIT_FAILURE);
    };

    //get the first line of csv file, should be single numeric value representing shop's balance
    getline(&line, &len, fp);
    //puts(line);
    //printf("***1\n");
    printf(line);
    //printf("\n***2\n");
    char *t = strtok(line, ",");
    double total = atof(t);
    printf("Budget from file %.2f \n", total);
    shop.cash = total;
    printf("Budget(cash) from shop struct %.2f\n", shop.cash);

    while ((read = getline(&line, &len, fp)) != -1)
    {
        //printf("%s - is line\n", line);
        printf(line);

        // printf(len);
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        char *name = malloc(sizeof(char) * 50);
        strcpy(name, n);
        int quantity = atoi(q);
        double price = atof(p);

        struct Product product = {name, price};
        struct ProductStock stockItem = {product, quantity};
        shop.stock[shop.index++] = stockItem;
        printf("NAME OF PRODUCT %s PRICE %.2f QUANT %d\n", name, price, quantity);
    };
    return shop;
};

void printShop(struct Shop s)
{
    printf("How much moneys? %f", s.cash);
    for (int i = 0; i < s.index; i++)
    {
        printProduct(s.stock[i].product);
        printf("The shop has %d of the above\n", s.stock[i].quantity);
    };
};

//check_stock checks for product name and then returns 0 (true) when product has enough quantity to meet customer order
//  else return 1 (false)
int check_stock(struct Shop * s, char * name, int quantity){
    for (int i = 0; i < s->index; i++)
    {
        if (strcmp(name, s->stock[i].product.name) == 0)
        {
            if (s->stock[i].quantity >= quantity)
            {
                return 0;
            }
            else
            {
                //print message to let customer know there is not enough quantity in stock of a particular product
                printf("Not enough stock of %s", s->stock[i].product.name);
                return 1;
            }
        }
    }
}

double find_price(struct Shop s, char *name)
{
    for (int i = 0; i < s.index; i++)
    {
        if (strcmp(name, s.stock[i].product.name) == 0)
        {
            return s.stock[i].product.price;
        }
    }
}

double find_price_p(struct Shop * s, char *name)
{
    for (int i = 0; i < s->index; i++)
    {
        if (strcmp(name, s->stock[i].product.name) == 0)
        {
            return s->stock[i].product.price;
        }
    }
}

void update_shop(struct Shop * s, char *name, int quantity_removed)
{
    //update shop cash with amount paid by customer
    //s->cash += cash_in;
    //loop through shop index to remove productStock quantity that customer is taking
    for (int i = 0; i < s->index; i++)
    {
        if (strcmp(name, s->stock[i].product.name) == 0)
        {
            //printf("%d - %d\n\n",s->stock[i].quantity,quantity_removed);
            s->stock[i].quantity = s->stock[i].quantity - quantity_removed;
            //printf("%d\n\n",s->stock[i].quantity);
        }
    }
}

void fulfill_order(struct Shop * s, struct Customer * cust)
{
    double order_total = 0.0;

    //printShop(myShop);
    int notenoughstock = 0;
    int insufficientfunds = 0;

    //Loop through customer order and determine if enough quantity and enough money
    for (int i = 0; i < cust->index; i++)
    {
        struct Product p = cust->shoppingList[i].product;
        double price = find_price_p(s, p.name);
        int quantity = cust->shoppingList[i].quantity;
        notenoughstock += check_stock(s,p.name,quantity);
        order_total = order_total + (price * quantity);
    }
    //if check_stock never returns a 1
    if (notenoughstock > 0){
        printf("Sorry there was not enough stock to make your order please try again.");
    }
    //else there was sufficient stock across every product requested
    else
    {
        //Next check that customer has enough money to pay for their order
        if (order_total > cust->budget)
        {
            printf("You don't have enough money, my apologies, please revise your order and try again.");
        }
        else
        {
            //Now Loop back through customer order and update the shop inventory as order is determined to be fulfillable
            for (int i = 0; i < cust->index; i++)
            {
                struct Product p = cust->shoppingList[i].product;
                int quantity = cust->shoppingList[i].quantity;
                update_shop(s,p.name,quantity);
            }
            printf("Shop balance before = %.2f\n", s->cash);
            s->cash += order_total;
            printf("Shop Balance After = %.2f\n", s->cash);
        }
    }
}

int main(void)
{
    // printf("The shop has %d of the product %s\n", bruStock.quantity, bruStock.product.name);
    //TODO Need to handle partially empty first line, basically done but recheck
    //TODO same with Customer to get their input, basically done now too
    struct Shop myShop = createAndStockShop();
    //printShop(myShop);

    struct Customer cust = createCustomerOrder("Customer Orders\\customer_order_a.csv");

    fulfill_order(&myShop,&cust);
    // double order_total = 0.0;

    // //printShop(myShop);
    // int notenoughstock = 0;
    // int insufficientfunds = 0;

    // //Loop through customer order and determine if enough quantity and enough money
    // for (int i = 0; i < cust.index; i++)
    // {
    //     struct Product p = cust.shoppingList[i].product;
    //     double price = find_price(myShop, p.name);
    //     int quantity = cust.shoppingList[i].quantity;
    //     notenoughstock += check_stock(&myShop,p.name,quantity);
    //     order_total = order_total + (price * quantity);
    // }
    // //if check_stock never returns a 1
    // if (notenoughstock > 0){
    //     printf("Sorry there was not enough stock to make your order please try again.");
    // }
    // //else there was sufficient stock across every product requested
    // else
    // {
    //     //Next check that customer has enough money to pay for their order
    //     if (order_total > cust.budget)
    //     {
    //         printf("You don't have enough money, my apologies, please revise your order and try again.");
    //     }
    //     else
    //     {
    //         //Now Loop back through customer order and update the shop inventory as order is determined to be fulfillable
    //         for (int i = 0; i < cust.index; i++)
    //         {
    //             struct Product p = cust.shoppingList[i].product;
    //             int quantity = cust.shoppingList[i].quantity;
    //             update_shop(&myShop,p.name,quantity);
    //         }
    //         printf("Shop balance before = %.2f\n", myShop.cash);
    //         myShop.cash += order_total;
    //         printf("Shop Balance After = %.2f\n", myShop.cash);
    //     }
    // }
    printShop(myShop);
    //printShop(myShop);
    //printf(a.name);

    //struct Customer emilyS = createCustomerOrder("customer_order_a.csv");
}

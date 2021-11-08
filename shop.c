#include <stdio.h>
#include <string.h>
#include <stdlib.h>
//Struct for a product e.g. struct Product irn_bru = {"Bottle Bru", 2.5};
struct Product {
    char* name;
    double price;
};

//Struct for amount of product in Stock
struct ProductStock {
    struct Product product;
    int quantity;
};

struct Shop {
    double cash;
    struct ProductStock stock[20];
    int index;
};

struct Customer {
    char* name;
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

void printCustomer(struct Customer c){
    printf("- - - - - - - - - - - - - -\n");
    printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f \n", c.name, c.budget);
    printf(" - - - - - - - - - - - - - \n");
    //in below for loop had to add index to customer struct to keep track of 
    for (int i=0; i<c.index; i++){
        printProduct(c.shoppingList[i].product);
        printf("%s ORDERS %d OF ABOVE PRODUCT\n",c.name,c.shoppingList[i].quantity);
        double cost = c.shoppingList[i].product.price*c.shoppingList[i].quantity;
        printf("The cost to %s will be %.2f\n", c.name, cost);
    };
}

struct Customer createCustomerOrder(char *file_loc){

    //printf(file_loc);
    //printf("See me");
    struct Customer cust;
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    size_t read;
    //fp=fopen(file_loc,"r");
    fp=fopen(file_loc,"r");
    if(fp==NULL){
        printf("file not found!");
        exit(EXIT_FAILURE);
    }

    //get the first line of csv file, should be single numeric value representing shop's balance
    getline(&line,&len,fp);

    //get customer name from first line of csv
    char *cn = strtok(line, ",");
    char *cust_name = malloc(sizeof(char) * 50);
    strcpy(cust_name,cn); //copy value from pointer into allocated memory
    cust.name = cust_name; //set struct name

    //get customer budget from first line of csv after first comma
    char *t = strtok(NULL,",");
    double total = atof(t); //convert string to double
    cust.budget = total;

    printf("Name from file %s \n",cust_name);
    printf("Budget from file %.2f \n",total);

    printf("Budget(cash) from cust struct %.2f\n",cust.budget);

    while((read=getline(&line,&len,fp)) != -1){
        //printf("%s - is line\n", line);
        //printf(line);
        // printf(len);
        char *n = strtok(line, ",");
        char *q = strtok(NULL, ",");
        char *name = malloc(sizeof(char) * 50);
        strcpy(name,n);
        int quantity = atoi(q);

        //struct Product product = {name,price};
        struct ProductStock stockItem = {name, quantity};
        cust.shoppingList[cust.index++] = stockItem;
        printf("NAME OF PRODUCT %s QUANT %d\n", name,  quantity);
    };
    return cust;
}

struct Shop createAndStockShop(){
    struct Shop shop = {200};
    FILE *fp;
    char *line = NULL;
    size_t len = 0;
    size_t read;
    //printf("YOO");
    fp = fopen("Shop Stock\\stock.csv","r");
    if(fp==NULL){
        printf("file not found");
        exit(EXIT_FAILURE);
    };

    //get the first line of csv file, should be single numeric value representing shop's balance
    getline(&line,&len,fp);
    //puts(line);
    //printf("***1\n");
    printf(line);
    //printf("\n***2\n");
    char *t = strtok(line,",");
    double total = atof(t);
    printf("Budget from file %.2f \n",total);
    shop.cash = total;
    printf("Budget(cash) from shop struct %.2f\n",shop.cash);

    while((read=getline(&line,&len,fp)) != -1){
        //printf("%s - is line\n", line);
        printf(line);

        // printf(len);
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        char *name = malloc(sizeof(char) * 50);
        strcpy(name,n);
        int quantity = atoi(q);
        int price = atof(p);

        struct Product product = {name,price};
        struct ProductStock stockItem = {product, quantity};
        shop.stock[shop.index++] = stockItem;
        printf("NAME OF PRODUCT %s PRICE %.2f QUANT %d\n", name, price, quantity);
    };
    return shop;
};

void printShop(struct Shop s){
    printf("How much moneys? %f", s.cash);
    for(int i=0;i<s.index;i++){
        printProduct(s.stock[i].product);
        printf("The shop has %d of the above\n", s.stock[i].quantity);
    };
};

int main(void)
{
    //printf("HERE");
    struct Customer keith = {"Keith", 3.50};
    //printCustomer(keith);

    struct Product irn_bru = {"Bottle Bru", 2.5};
    struct ProductStock bruStock = {irn_bru,20};
    //printProduct(irn_bru);

    struct Product plastic = {"Plastic Bag", 1.00};
    struct ProductStock plasticStock = {plastic,10};

    //keith.index should initialize to 0, thereafter it keeps track of how many shopping list items
    //shoppingList[0] in this case will be 20 irn_bru Products
    //shoppingList[1] would be some other product
    keith.shoppingList[keith.index++] = bruStock;
    keith.shoppingList[keith.index++] = plasticStock;
    //printCustomer(keith);

   // printf("The shop has %d of the product %s\n", bruStock.quantity, bruStock.product.name);
    //TODO Need to handle partially empty first line, basically done but recheck
    //TODO same with Customer to get their input, basically done now too
    struct Shop myShop = createAndStockShop();
    printShop(myShop);

    struct Customer a = createCustomerOrder("Customer Orders\\customer_order_a.csv");


    printShop(myShop);
    //printf(a.name);

    //struct Customer emilyS = createCustomerOrder("customer_order_a.csv");
}

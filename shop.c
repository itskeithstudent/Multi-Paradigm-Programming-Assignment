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

struct QuantityUpdate
{
    int update;
    int quantity;
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
        printf("\nproduct=%s\n",c.shoppingList[i].product.name);
        printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
        double cost = c.shoppingList[i].product.price * c.shoppingList[i].quantity;
        printf("The cost to %s will be %.2f\n", c.name, cost);
    };
}

// void summariseCustomerPurchase(struct Customer c)
// {
//     printf("- - - - - - - - - - - - - -\n");
//     printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: %.2f \n", c.name, c.budget);
//     printf(" - - - - - - - - - - - - - \n");
    
//     for (int i = 0; i < c.index; i++)
//     {
//         printProduct(c.shoppingList[i].product);
//         printf("%s ORDERS %d OF ABOVE PRODUCT\n", c.name, c.shoppingList[i].quantity);
//         double cost = c.shoppingList[i].product.price * c.shoppingList[i].quantity;
//         printf("The cost to %s will be %.2f\n", c.name, cost);
//     };
// }

struct Customer createCustomerOrder(char *file_loc)
{

    //printf(file_loc);
    //printf("See me");
    struct Customer cust;
    printf("cust index %d",cust.index);
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

    // printf("Name from file %s \n", cust_name);
    // printf("Budget from file %.2f \n", total);

    // printf("Budget(cash) from cust struct %.2f\n", cust.budget);
    printf("cust index %d",cust.index);
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
        printf("cust index %d",cust.index);
        cust.shoppingList[cust.index++] = stockItem;
        printf("cust index %d",cust.index);
        // printf("STRUCT NAME OF PRODUCT %s QUANT %d\n", stockItem.product.name, stockItem.quantity);
        // printf("NAME OF PRODUCT %s QUANT %d\n", name, quantity);
    };
    return cust;
}

struct Customer createLiveCustomerOrder()
{
    struct Customer cust;
    cust.index = 0; //ensure customer index correct
    fflush(stdin);
    printf("Please enter your name: ");

    char * cust_name = malloc(sizeof(char) * 50);
    scanf("%s", cust_name);
    cust.name = cust_name;
    // printf("%s", cust_name);

    double cust_budget;
    printf("Please enter your budget: ");
    scanf("%lf", &cust_budget);
    cust.budget = cust_budget;
    // printf("%lf", cust_budget);

    char * product_choice = malloc(sizeof(char) * 50);
    char * product_name = malloc(sizeof(char) * 50);
    printf("\nEnter name of product or 0 to stop \n");
    //fflush(stdin);
    getchar(); //clear newline left over from scanf
    fgets(product_choice,50, stdin);
    
    int len=strlen(product_choice); //get len of product_choice
    //if product_choice ends in '\n' new line replace
    if(product_choice[len-1]=='\n'){
        product_choice[len-1]='\0';
    }

    while (strcmp(product_choice,"0")){
        struct Product productDetail;
        char * product_name = malloc(sizeof(char) * 50);
        strcpy(product_name,product_choice);
        productDetail.name = product_name;

        int quantity;
        printf("Enter quantity of %s to order \n", product_choice);
        scanf("%d", &quantity);
        struct ProductStock stockItem;
        stockItem.product=productDetail;
        stockItem.quantity=quantity;
        printf("%s, %lf, %d\n\n", productDetail.name, productDetail.price, quantity );
        printf("\n***********************************************************\n");
        cust.shoppingList[cust.index++] = stockItem;
        printf("Enter name of product or 0 to stop \n");
        //ensure no \n to mess up fgets
        fflush(stdin);
        getchar();

        fgets(product_choice,50, stdin);
        int len=strlen(product_choice);
        //eliminate any newline character
        if(product_choice[len-1]=='\n'){
            product_choice[len-1]='\0';
        }
    }
    printf("cust.index - %d", cust.index);
    printf("index 0 - \n%s\n\n",cust.shoppingList[0].product.name);
    printf("index 1 - \n%s\n\n",cust.shoppingList[1].product.name);
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
    // printf("Budget from file %.2f \n", total);
    shop.cash = total;
    // printf("Budget(cash) from shop struct %.2f\n", shop.cash);

    while ((read = getline(&line, &len, fp)) != -1)
    {
        //printf("%s - is line\n", line);
        // printf(line);

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
        // printf("NAME OF PRODUCT %s PRICE %.2f QUANT %d\n", name, price, quantity);
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
            printf("Checking shop stock of %s, quantity in stock - %d\n", s->stock[i].product.name, s->stock[i].quantity);
            if (s->stock[i].quantity >= quantity)
            {
                return quantity;
            }
            else
            {
                //print message to let customer know there is not enough quantity in stock of a particular product
                //printf("Not enough stock of %s, changing quantity to match what shop has in stock - %d\n", s->stock[i].product.name, s->stock[i].quantity);
                return s->stock[i].quantity;
            }
        }
    }
    printf("We don't stock this item.");
    return 0;
}


//find_price, looks for product name in Shop struct
//returns orice of product
double find_price(struct Shop * s, char *name)
{
    for (int i = 0; i < s->index; i++)
    {
        if (strcmp(name, s->stock[i].product.name) == 0)
        {
            return s->stock[i].product.price;
        }
    }
}

//update_shop, looks for product by name and reduces quantity in stock
//returns nothing, acts on Shop stuct in-place
void update_shop(struct Shop * s, char *name, int quantity_removed)
{
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

//fulfill_order takes in pointer arguments for struct for Shop and struct for Customer
//checks Shop struct for requested products and corrects Customer struct with correct quantities if too many requested
//if customer has enough in their budget, order is placed, with shop quantities in stock updated and shop cash increased
//updates all structs in-place
void fulfill_order(struct Shop * s, struct Customer * cust)
{
    double order_total = 0.0;
    printf("\n___________________________________________________________________\n");
    printf("Hello %s, I'll now start processing your order!", cust->name);
    printf("\n===================================================================\n\n");
    //Loop through customer order and determine if enough quantity and enough money
    //if requesting too much quantity, update the order to suit what shop has (even if shop has 0 quantity)
    for (int i = 0; i < cust->index; i++)
    {
        struct Product p = cust->shoppingList[i].product;
        double price = find_price(s, p.name);
        //checked_quantity stores the quantity returned from check_stock, which is either the original quantity requested (if in-stock) or whatever stock the shop has
        int checked_quantity = check_stock(s,p.name,cust->shoppingList[i].quantity);
        printf("Customer has requested %d of %s, actual quantity that can be provided %d\n\n", cust->shoppingList[i].quantity, p.name, checked_quantity);
        cust->shoppingList[i].quantity = checked_quantity;
        //order_total will be what is subtracted from customer budget and added to shop cash
        order_total = order_total + (price * checked_quantity);
    }
    //Next check that customer has enough money to pay for their order
    if (order_total > cust->budget)
    {
        printf("\n===================================================================\n");
        printf("You don't have enough money, my apologies, please revise your order and try again.");
        printf("\n___________________________________________________________________\n");
    }
    else
    {
        //Now Loop back through customer order and update the shop inventory as order is determined to be fulfillable
        printf("\n===================================================================\n");
        printf("Thank you for your custom, that will be %.2f total please.", order_total);
        printf("\n___________________________________________________________________\n");
        for (int i = 0; i < cust->index; i++)
        {
            struct Product p = cust->shoppingList[i].product;
            int quantity = cust->shoppingList[i].quantity;
            update_shop(s,p.name,quantity);
        }
        s->cash += order_total;
    }
}

int main(void)
{
    // printf("The shop has %d of the product %s\n", bruStock.quantity, bruStock.product.name);
    //TODO Need to handle partially empty first line, basically done but recheck
    //TODO same with Customer to get their input, basically done now too
    struct Shop myShop = createAndStockShop();
    //printShop(myShop);

    int choice = -1;

	while (choice != 0){
		fflush(stdin);
		printf("\nPlease choose an option:\n(1) Normal customer order\n(2) Customer order with not enough money\n(3) Customer order with excess quantity\n(4) Live Order\n(0) Exit Shop\n");
		scanf("%d", &choice);

		if (choice == 1)
		{
            struct Customer custom_order = createCustomerOrder("Customer Orders\\customer_order_a.csv");
            // printf("\n%f",custom_order.budget);
            // printf("\nAAA %s", custom_order.shoppingList[1].product.name);
            // printf("\nBBB%s", custom_order.shoppingList[0].product.name);
            fulfill_order(&myShop,&custom_order);
		} else if (choice == 2){
            struct Customer custom_order = createCustomerOrder("Customer Orders\\customer_order_b.csv");
            fulfill_order(&myShop,&custom_order);
		} else if (choice == 3){
            struct Customer custom_order = createCustomerOrder("Customer Orders\\customer_order_c.csv");
            fulfill_order(&myShop,&custom_order);
		} else if (choice == 4){
            struct Customer custom_order = createLiveCustomerOrder();
            printf("\n%f",custom_order.budget);
            printf("\nAAA %d", custom_order.shoppingList[0].product.name);
            printf("\nBBB %d", custom_order.shoppingList[0].quantity);
            fulfill_order(&myShop,&custom_order);
        }
	}
	printf("Buh bye");
}

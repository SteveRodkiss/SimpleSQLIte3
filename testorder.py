"""basic functionality for a simple pizza ordering system with sqlite databse storage"""
import sqlite3

def print_menu(connection):
    """print the menu out so we can easilt see what pizza to pick"""
    c = connection.cursor()
    c.execute("SELECT id,name FROM pizzas")
    results = c.fetchall()
    for entry in results:
        print("{0:<4} {1:<30}".format(entry[0],entry[1]))


def insert_order_name(connection, name):
    """insert the order into the pizzaorders and return the id of the order"""
    c = connection.cursor()
    sql = "INSERT INTO orders (ordername,ordertime) VALUES (?,time('now'))"
    c.execute(sql,(name,))
    connection.commit()
    #get the id of the last entry
    return c.lastrowid

def insert_pizza_into_order(connection, orderid, pizzaid):
    """Insert a particular pizza attached to a particular order into the bridging table"""
    c = connection.cursor()
    sql = "INSERT INTO pizzaorders (orderid,pizzaid) VALUES (?,?)"
    c.execute(sql,(orderid,pizzaid))
    connection.commit()

def display_order_by_name(connection, name):
    """display the pizza's order by a particular customer from their name"""
    #get the orders and names
    #print all the pizzas that are associated to the name
    c = connection.cursor()
    #whey! huge sql statement
    sql = "SELECT pizzas.name FROM pizzaorders JOIN orders ON orders.id=pizzaorders.orderid JOIN pizzas ON pizzas.id=pizzaorders.pizzaid WHERE orders.ordername = ?"
    c.execute(sql,(name,))
    results = c.fetchall()
    if len(results) == 0:
        print("There doesn't seem to be any pizzas ordered by that person\n")
        return
    print("Pizzas in {0}'s order: ".format(name))
    #iterate through the list of tuples
    pizzanum = 1
    for pizza in results:
        #display the first (and only) element of the tuple- the pizza name
        print("Pizza Number {0} : {1}".format(pizzanum,pizza[0]))
        pizzanum += 1

def make_an_order(connection):
    """big function to get an actual order name and use the other functions to insert the data into orders and pizzaorders"""
    #get the order name
    name = input("What is the order name?: ")
    #get the order id back from the insert
    orderid = insert_order_name(connection,name)
    #loop through all the pizza orders
    print("What pizza would you like?")
    while True:
        #print the menu out
        print_menu(connection)
        print("0    to exit")
        #get the order
        pizzanum = int(input("Pizza Number: "))
        if pizzanum == 0:
            break
        #insert it into the database
        insert_pizza_into_order(connection,orderid,pizzanum)
        #ans ask if they want another
        print("Next pizza? ")

def display_all_orders(connection):
    """list all the names of all the people who have placed orders and the times they did it"""
    c = connection.cursor()
    sql = "SELECT ordername,ordertime FROM orders"
    c.execute(sql)
    results = c.fetchall()
    for order in results:
        print("Name: {0:<18} Time:{1:<16}".format(order[0],order[1]))


if __name__ == "__main__":
    #get the connection
    connection = sqlite3.connect("shop1.db")
    while True:
        action = input("\nWhat would you like to do?\n1. Make an order\n2. Find and order\n3. Exit\n-- ")
        if action == "1":
            make_an_order(connection)
        elif action == "2":
            display_all_orders(connection)
            name = input("Whose order do you want to view?: ")
            display_order_by_name(connection,name)
        elif action == "3":
            print("Goodbye")
            break
        else:
            print("Please make a valid choice")




    
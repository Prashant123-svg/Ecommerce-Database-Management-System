import Database 

# database connection establised

from customers import Customers
from products import Products
from sales import Sales

def main_menu():
    while True:
        print("1. Customers Management")
        print("2. Products Management")
        print("3. Sales Management")
        print("0. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            customers = Customers()
            customers.customers_menu()
        elif choice == '2':
            products = Products()
            products.products_menu()
        elif choice == '3':
            sales = Sales()
            sales.sales_menu()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            
if __name__ == "__main__":
    main_menu()            
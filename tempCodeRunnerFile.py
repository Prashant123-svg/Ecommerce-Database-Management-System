import psycopg2
from Database import con

class Customers:
   def __init__(self):
     pass
    #  self.name=name
    #  self.contact=contact
     
   def create_table(self):
      cur=con.cursor()
      cur.execute("""CREATE TABLE IF NOT EXIST Customers(id SERIAL PRIMARY KEY,name VARCHAR(100) NOTNULL, contact VARCHAR(15) NOTNULL)""")
      con.commit()
      cur.close()
      
   def insert_customer(self,name,contact):  
     cur=con.cursor()
     cur.execute("""INSERT INTO customers(name,contact) VALUES(%S,%S)""",(name,contact))
     con.commit
     cur.close()
     
   def update_customer(self,customer_id,name=None,contact=None):
    cur=con.cursor()
    cur.execute("SELECT * FROM customers WHERE id=%s",(customer_id))
    customers=cur.fetchall()
    if not customers:
        print(">>>> Customer Not Found!")
        cur.close()
        return
    update_fields=[]
    if name:
      update_fields.append(f"name='{name}")
    if contact:
       update_fields.append(f"contact='{contact}")
    Update_query=f"UPDATE customers SET {','.join(update_fields)} WHERE id=%s"
    cur.execute(Update_query,(customer_id,))     
    con.commit()
    cur.close()
    
    def delete_customer(self,customer_id):
      cur=con.cursor()
      cur.execute("""DELETE FROM customers WHERE id=%s""",(customer_id,))
      con.commit()
      cur.close()
      
    def get_all_customers(self):
      cur=con.cursor()
      cur.execute("SELECT * FROM customers")
      customers=cur.fetchall()
      cur.close()
      return customers
    
    def customers_menu(self):
      customer=Customers()
      while True:
        print("1. Create Customers Table")
        print("2. Insert Customer")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Show All Customers")
        print("6. Exit")
        choice=input("Enter your choice:")
        if choice == '1':
          customer.create_table()
          print(">>>> Customers Table Created Successfully!")
        elif choice=='2':
          name=input('Enter Customer Name: ')
          contact=input('Enter customer contact :')
          customer.insert_customer(name,contact)
          print(">>>> customer Inserted Successfully")
        elif choice=='3':
          customer_id=int(input("Enter Customer Id to Update: "))
          name=input("Enter New Name (Leave blank to keep unchanged): ")
          contact=input("Enter New Contact (Leave blank to keep unchanged): ")
          customer.update_customer(customer_id,name if name else None,contact if contact else None)
          print(">>>> Customer Updated Successfully!")
        elif choice=='4':
          customer_id=int(input("Enter Customer Id to Delete : "))
          customer.delete_customer(customer_id)
          print(">>>> Customer Deleted Successfully")
        elif choice=='5':
          customers=customer.get_all_customers()
          if customers:
            print(">>>> All customers: ")
            for customer in customers:
              print(f"ID: {customer[0]}, Name: {customer[1]}, Contact: {customer[2]}")
            else: 
              print(">>>> No Customers Found!: ")
          elif choice =='6':
            print(">>>> Exiting Customers Menu: ")
            break
          else:
            print(">>>> Invalid Choice! Please Try Again.")
            
      customer.customers_menu()
            
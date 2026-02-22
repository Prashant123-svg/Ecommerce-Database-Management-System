from Database import con

class Products:
  def __init__(self):
    pass
  
  @staticmethod
  def create_table():
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS products(id SERIAL PRIMARY KEY,name VARCHAR(50) NOT NULL,description TEXT NOT NULL,price DECIMAL(10,2) NOT NULL,quantity INTEGER NOT NULL)""")
    con.commit()
    cur.close()
    
  @staticmethod
  def insert_products(name,description,price,quantity):   
    cur=con.cursor()
    cur.execute("""INSERT INTO products(name,description,price,quantity) VALUES(%s,%s,%s,%s)""",(name,description,price,quantity))
    con.commit()
    cur.close()
    
  @staticmethod
  def update_products(product_id,name=None,description=None, price=None,quantity=None):
      cur=con.cursor()
      cur.execute("""SELECT * FROM products WHERE id=%s""",(product_id,))
      product=cur.fetchone()
      if not product:
        print(">>>> product Not Found! ")
        cur.close()
        return
      update_fields=[]
      if name:
        update_fields.append(f"name='{name}'")
      if description:
        update_fields.append(f"description='{description}'")
      if price:
        update_fields.append(f"price='{price}'")
      if quantity is not None:
        update_fields.append(f"quantity='{quantity}'")
      
      if update_fields:
        update_query=f"UPDATE products SET {', '.join(update_fields)} WHERE id=%s"
        cur.execute(update_query,(product_id,))
        con.commit()
      cur.close()
  @staticmethod
  def delete_products(product_id):
    cur=con.cursor()
    cur.execute("""DELETE FROM products WHERE id=%s""",(product_id,))
    con.commit()
    cur.close()
    
  @staticmethod
  def get_all_products():
    cur=con.cursor()
    cur.execute("""SELECT * FROM products""")
    products=cur.fetchall()
    cur.close()  
    return products
  
  @staticmethod
  def view_product_id(product_id):
    cur=con.cursor()
    cur.execute("""SELECT * FROM products WHERE id=%s""",(product_id,))
    product=cur.fetchone()
    cur.close()
    return product
    
  @staticmethod
  def View_products():
    cur=con.cursor()
    cur.execute("""SELECT * FROM products""")
    products=cur.fetchall()
    cur.close()
    return products
  
  def products_menu(self):
    product=Products()
    while True:
      print("1. Create Products Table")
      print("2. Insert Product")
      print("3. Update Product")
      print("4. Delete Product")
      print("5. Show All Products")
      print("0. Exit")
      choice=input("Enter your choice:")
      if choice == '1':
        product.create_table()
        print(">>>> Products Table Created Successfully!")
      elif choice=='2':
        name=input('Enter Product Name: ')
        description=input('Enter Product Description: ')
        price=float(input('Enter Product Price: '))
        quantity=int(input('Enter Product Quantity: '))
        product.insert_products(name,description,price,quantity)
        print(">>>> Product Inserted Successfully!")
      elif choice=='3':
        product_id=int(input("Enter Product Id to Update: "))
        name=input('Enter New Product Name (leave blank to keep unchanged): ')
        description=input('Enter New Product Description (leave blank to keep unchanged): ')
        price_input=input('Enter New Product Price (leave blank to keep unchanged): ')
        quantity_input=input('Enter New Product Quantity (leave blank to keep unchanged): ')
        price=float(price_input) if price_input else None
        quantity=int(quantity_input) if quantity_input else None
        product.update_products(product_id,name,description,price,quantity)
        print(">>>> Product Updated Successfully!")
      elif choice=='4':
         product_id=int(input("Enter Product Id to Delete: "))
         product.delete_products(product_id)
         print(">>>> Product Deleted Successfully!")
      elif choice=='5':
         products=product.View_products()
         for prod in products:
            print(f"ID: {prod[0]}, Name: {prod[1]}, Description: {prod[2]}, Price: {prod[3]}, Quantity: {prod[4]}")
      elif choice=='0':
         break
      else:
         print(">>>> Invalid Choice! Please Try Again.")
         
#Products().products_menu()         
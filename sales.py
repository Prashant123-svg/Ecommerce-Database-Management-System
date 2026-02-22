from Database import con

class Sales:
  def __init__(self):
    pass
  
  @staticmethod
  def create_table():
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS sales(
      id SERIAL PRIMARY KEY,
      customer_id INTEGER NOT NULL,
      date DATE NOT NULL, 
      total_amount DECIMAL(10,2) NOT NULL,
      FOREIGN KEY (customer_id) REFERENCES Customers(id) ON DELETE CASCADE
    )""")
    con.commit()
    cur.close()
    
  @staticmethod  
  def insert_sale(customer_id,date,total_amount):
    cur=con.cursor()
    cur.execute("""INSERT INTO sales(customer_id,date,total_amount) VALUES(%s,%s,%s)""",(customer_id,date,total_amount))  
    con.commit()
    cur.close()
    
  @staticmethod
  def update_sale(sale_id,customer_id=None,date=None,total_amount=None):
    cur=con.cursor()
    cur.execute("""SELECT * FROM sales WHERE id=%s""",(sale_id,))
    sale=cur.fetchone()
    if not sale:
      print(">>>> Sale Not Found! ")
      cur.close()
      return
    update_fields=[]
    if customer_id:
      update_fields.append(f"customer_id='{customer_id}'")
    if date:
      update_fields.append(f"date='{date}'")
    if total_amount:
      update_fields.append(f"total_amount='{total_amount}'")
    
    if update_fields:
      update_query=f"UPDATE sales SET {', '.join(update_fields)} WHERE id=%s"
      cur.execute(update_query,(sale_id,))
      con.commit()
    cur.close()
      
  @staticmethod
  def delete_sale(sale_id):
    cur=con.cursor()
    cur.execute("""DELETE FROM sales WHERE id=%s""",(sale_id,))
    con.commit()
    cur.close()
    
  @staticmethod
  def generate_bill(sale_id):
    cur=con.cursor()
    cur.execute("""SELECT * FROM sales WHERE id=%s""",(sale_id))
    sale_items=cur.fetchall()
    total_amount=0
    for item in sale_items:
      total_amount+=item[4]*item[3] 
    cur.close()
    return total_amount
  
  @staticmethod
  def view_sales():
    cur=con.cursor()
    cur.execute("""SELECT * FROM sales""")
    sales=cur.fetchall()
    cur.close()
    return sales
  
  @staticmethod
  def view_sale_id(sale_id):
    cur=con.cursor()
    cur.execute("""SELECT * FROM sales WHERE id=%s""",(sale_id,))
    sale=cur.fetchone()
    cur.close()
    return sale
  
  # Analysis Queries
  @staticmethod
  def total_sales_by_date(starting_date,ending_date):
    cur=con.cursor()
    cur.execute("""SELECT SUM(total_amount) FROM sales WHERE date BETWEEN %s AND %s""",(starting_date,ending_date))
    total_sales=cur.fetchone()[0]
    cur.close()
    return total_sales
  
  @staticmethod
  def top_selling_products():
    cur=con.cursor()
    cur.execute("""SELECT product_id,SUM(quantity) AS total_quantity FROM sales GROUP BY product_id ORDER BY total_quantity DESC LIMIT 5""")
    top_products=cur.fetchall()
    cur.close()
    return top_products
  
  
  def sales_menu(self):
      sales=Sales()
      while True:
        print("1. Create Sales Table")
        print("2. Insert Sale")
        print("3. Update Sale")
        print("4. Delete Sale")
        print("5. Generate Bill")
        print("6. View All Sales")
        print("7. View Sale by ID")
        print("8. Total Sales by Date Range")
        print("9. Top Selling Products")
        print("0. Exit")
        choice=input("Enter your choice: ")
        if choice=='1':
          sales.create_table()
          print(">>>> Sales Table Created Successfully!")
        elif choice=='2':
          customer_id=int(input("Enter Customer ID: "))
          date=input("Enter Sale Date (YYYY-MM-DD): ")
          total_amount=float(input("Enter Total Amount: "))
          sales.insert_sale(customer_id,date,total_amount)
          print(">>>> Sale Inserted Successfully!")
        elif choice=='3':
          sale_id=int(input("Enter Sale ID to Update: "))
          customer_id=int(input("Enter New Customer ID (Leave blank to keep unchanged): ") or 0)
          date=input("Enter New Sale Date (YYYY-MM-DD) (Leave blank to keep unchanged): ")
          total_amount=float(input("Enter New Total Amount (Leave blank to keep unchanged): ") or 0)
          sales.update_sale(sale_id,customer_id if customer_id else None,date if date else None,total_amount if total_amount else None)
          print(">>>> Sale Updated Successfully!")
        elif choice=='4':
          sale_id=int(input("Enter Sale ID to Delete: "))
          sales.delete_sale(sale_id)
          print(">>>> Sale Deleted Successfully!")
        elif choice=='5':
          sale_id=int(input("Enter Sale ID to Generate Bill: "))
          total_amount=sales.generate_bill(sale_id)
          print(f">>>> Total Amount for Sale ID {sale_id}: {total_amount}")
        elif choice=='6':
          all_sales=sales.view_sales()
          if all_sales:
            print(">>>> All Sales: ")
            for sale in all_sales:
              print(f"ID: {sale[0]}, Customer ID: {sale[1]}, Date: {sale[2]}, Total Amount: {sale[3]}")
          else:
            print(">>>> No Sales Found!")
        elif choice=='7':
          sale_id=int(input("Enter Sale ID to View: "))
          sale=sales.view_sale_id(sale_id)
          if sale:
            print(f"ID: {sale[0]}, Customer ID: {sale[1]}, Date: {sale[2]}, Total Amount: {sale[3]}")
          else:
            print(">>>> Sale Not Found!")
        elif choice=='8':
          starting_date=input("Enter Starting Date (YYYY-MM-DD): ")
          ending_date=input("Enter Ending Date (YYYY-MM-DD): ")
          total_sales=sales.total_sales_by_date(starting_date,ending_date)
          print(f">>>> Total Sales from {starting_date} to {ending_date}: {total_sales}")
        elif choice=='9':
          top_products=sales.top_selling_products()
          if top_products:
            print(">>>> Top Selling Products: ")
            for product in top_products:
              print(f"Product ID: {product[0]}, Total Quantity Sold: {product[1]}")
          else:
            print(">>>> No Sales Found!") 
        elif choice=='0':
          break
        else:
          print(">>>> Invalid Choice! Please Try Again.")   
    
# Sales().sales_menu()            
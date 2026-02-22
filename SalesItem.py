from Database import con

class SalesItem:
    def __init__(self):
      pass
      #  self.name=name
      #  self.price=price
    @staticmethod
    def create_table():
        cur=con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS SalesItem(
            id SERIAL PRIMARY KEY,
            sale_id INTEGER NOT NULL, 
            product_id INTEGER NOT NULL, 
            quantity INTEGER NOT NULL, 
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )""")
        con.commit()
        cur.close()
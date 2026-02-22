import psycopg2
def connection():
    con = psycopg2.connect(
      host="localhost",
      database="ecommerce",
      user="postgres",
      password="admin",
      port="5432"
    )  
    if con:
      print(">>> connection Establised!")
    else:
      print(">>>>Connection failed!")
    return con  
  
con = connection()    
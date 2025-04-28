import mysql.connector
import pandas as pd




class Database:
    def __init__(self):

        self.config = {
            "host":"localhost",
            "user":"root",
            "password":"Velkommen25",
            "database": "ugedata"
        }
        self.execute_Database()
        self._connection = self.connection()
        
        self.create_table()
        self.insert_csv_products()
        self.insert_csv_customers() 

        self.insert_csv_orders() 

        self.drop_Database()
    
    def execute_Database(self):
        try:
            temp = mysql.connector.connect(host=self.config["host"],user=self.config["user"],password=self.config["password"])
            cursor = temp.cursor() 

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config["database"]}")
            print("create database")
            cursor.close()
            temp.close()
        except mysql.connector.Error as err:
            print(f"connection didn't work {err}")
    
    def connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                print("you are connections")
                return connection
        except mysql.connector.Error as err:
            print(f"connection didn't work {err}")
            return None

    def create_table(self):
        if not self._connection.is_connected():
            print("you are not connection database")
        
        try:
            cursor = self._connection.cursor()

            cursor.execute("""  
                                CREATE TABLE IF NOT EXISTS customers
                                (
                                  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255) NOT NULL, 
                                email VARCHAR(225) NOT NULL
                                )
                           """)
            cursor.execute("""  
                                CREATE TABLE IF NOT EXISTS products
                                (
                                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255) NOT NULL, 
                                price INT NOT NULL
                                )
                           """)
            cursor.execute("""  
                                CREATE TABLE IF NOT EXISTS orders(
                                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                    date_time VARCHAR(255) NOT NULL,  
                                    customer_id INT NOT NULL,
                                    product_id INT NOT NULL,
                                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                                    FOREIGN KEY(product_id) REFERENCES products(id)
                                )
                            """)
        except mysql.connector.Error as err:
            print(f"you connection to create table: {err}")
            
    def insert_csv_customers(self):
       
        df = pd.read_csv("../data/customers.csv")
       
        if not self._connection.is_connected():
            print("you are not connection database")

        try:
            # df = df.iloc[:, 1:]  
            data = list(df.itertuples(index=False,name=None))
       
            query = "INSERT INTO customers(id,name,email) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email)"

            cursor = self._connection.cursor()

            cursor.executemany(query,data)
            self._connection.commit()

            print(f"Record insert successful in customers")
        except mysql.connector.Error as err:
            print(f"something went wrong in csv_customers {err}")

    def insert_csv_products(self):
       
        df = pd.read_csv("../data/products.csv")
       
        if not self._connection.is_connected():
            print("you are not connection database")

        try:
            # df = df.iloc[:, 1:]  
            data = list(df.itertuples(index=False,name=None))
       
            query = "INSERT INTO products(id,name,price) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name), price=VALUES(price)"

            cursor = self._connection.cursor()

            cursor.executemany(query,data)
            self._connection.commit()

            print(f"Record insert successful in products")
        except mysql.connector.Error as err:
            print(f"something went wrong in csv_products {err}")

    def insert_csv_orders(self):
       
        df = pd.read_csv("../data/orders.csv")
       
        if not self._connection.is_connected():
            print("you are not connection database")
       
        try:
            cursor = self._connection.cursor()

            cursor.execute("SELECT id FROM customers")
            valid_customers = {row[0] for row in cursor.fetchall()}
            
            cursor.execute("SELECT id FROM products")
            valid_products = {row[0] for row in cursor.fetchall()}
            
            df = df[df["product"].isin(valid_products)]
            df = df[df["customer"].isin(valid_customers)]

            if df.empty:
                print("No valid orders to insert.")
                return   

            data = list(df[["id", "date_time", "customer", "product"]].itertuples(index=False, name=None))
            query = """INSERT INTO orders(id,date_time,customer_id,product_id) 
                        VALUES(%s,%s,%s,%s) 
                        ON DUPLICATE KEY UPDATE 
                            date_time=VALUES(date_time), 
                            customer_id=VALUES(customer_id), 
                            product_id=VALUES(product_id)
                         """
            
            cursor = self._connection.cursor()
            cursor.executemany(query,data)
            self._connection.commit()

            print(f"Record insert successful in Orders")
        except mysql.connector.Error as err:
            print(f"something went wrong in csv_orders {err}")


    def modify_table_auto_id(self):
        if not self._connection.is_connected():
            print("you are not connection database")
            return

        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT MAX(id) FROM customers;")
            max_id = cursor.fetchone()[0]  

            if max_id:  
                cursor.execute(f"ALTER TABLE customers AUTO_INCREMENT = {max_id + 1};")

            self._connection.commit()

        except mysql.connector.Error as err:
            print(f" Error AUTO_INCREMENT: {err}")


    def insert_customer(self,name,email):
        if not self._connection.is_connected():
            print("you are not connection database")
            return
        # try:
        cursor = self._connection.cursor()
        query = """ 
            INSERT INTO customers (name, email) 
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email)
        """
        cursor.execute(query,(name,email))
        self._connection.commit()
        print(f"add customer name: {name} and email {email}")

    def drop_Database(self):
        try:
    
            if self._connection.is_connected():
                self._connection.close()
                print("Closed connection to data")

            temp = mysql.connector.connect(
                host= self.config["host"],
                user=self.config["user"],
                password=self.config["password"]
            )

            cursor = temp.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.config['database']}")
            print(f"Dropped database complete")
            cursor.close()
            temp.close()
            
        except mysql.connector.Error as err:
            print(f"There was Error when try dropped database {err}")
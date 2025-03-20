from mysql.connector.connection import MySQLConnection
from tabulate import tabulate

class Orders:
    def __init__(self,connection:MySQLConnection):
        self._connections = connection

        self._cursor = connection.cursor()    
        self._cursor.execute("SHOW TABLES")

    def Fetch_Tables_name(self):
       
        tables = self._cursor.fetchall()
        for table in tables:
            print(table[0])

    def fetch_headers(self)-> list:
        self._cursor.execute("SHOW COLUMNS FROM orders")
        columns = []
        for column in self._cursor.fetchall():
            columns.append(column[0])
        return columns
    
    def fetch_orders_rows(self,amount):
        self._cursor.execute(f"SELECT * FROM orders LIMIT {amount}")
        rows = self._cursor.fetchall()
        return rows
    
    def fetch_data(self,amount:int):
        headers = self.fetch_headers()

        rows = self.fetch_orders_rows(amount)
        print(tabulate(rows,headers,tablefmt='grid'))
    
    

import mysql.connector
from orders import Orders 
from database import Database


class Connect:
    def __init__(self):
        self._connection = None
        self._db = Database()
        self.connect()

        if self._connection:
            # self.excucte_queue_orders()
            self.disconnect()

        
    

    def connect(self):
        try:
            self._connection = mysql.connector.connect(host='localhost',user='root',password='Velkommen25',database='uge4data')
                

        except mysql.connector.Error as err:
            print(f"Connection Error: {err}")
    

    def excucte_queue_orders(self):
         
         if not self._connection:
            print("there are no connection")

         orders = Orders(self._connection)

         orders.Fetch_Tables_name()
         orders.fetch_data(15)

    def disconnect(self):
        if self._connection and self._connection.is_connected():
             self._connection.close()
        print("Connection closed")



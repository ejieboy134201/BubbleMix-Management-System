import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def add_item(self, product_name, price, quantity):
        self.cursor.execute('INSERT INTO inventory (product_name, price, quantity) VALUES (?, ?, ?)',
                            (product_name, price, quantity))
        self.connection.commit()

    def update_item_quantity(self, product_name, quantity):
        self.cursor.execute('UPDATE inventory SET quantity = quantity - ? WHERE product_name = ?',
                            (quantity, product_name))
        self.connection.commit()

    def get_inventory(self):
        self.cursor.execute('SELECT * FROM inventory')
        return self.cursor.fetchall()

    def record_sale(self, product_name, product_quantity, product_price, total_amount):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('INSERT INTO sales_report (date, product_name, product_quantity, product_price, total_amount) VALUES (?, ?, ?, ?, ?)',
                            (date, product_name, product_quantity, product_price, total_amount))
        self.connection.commit()

    def close(self):
        self.connection.close()

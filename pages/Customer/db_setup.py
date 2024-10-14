import sqlite3

def setup_database():
    conn = sqlite3.connect('database/Ordering_system.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales_report (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_quantity INTEGER NOT NULL,
        product_price REAL NOT NULL,
        total_amount REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()

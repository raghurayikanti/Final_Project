
import sqlite3

def setup_database():
    """Initialize and configure the database schema."""
    with sqlite3.connect("db.sqlite") as conn:  # Match DB_FILE from main.py
        cursor = conn.cursor()

        # Table for storing customer details
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL
            )
        """)

        # Table for storing items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL
            )
        """)

        # Table for storing orders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                notes TEXT,
                timestamp INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        # Table for storing ordered items
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)

        print("Database tables are set up successfully.")

if __name__ == "__main__":
    setup_database()

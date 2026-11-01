
import sqlite3
from pathlib import Path

# Create SQLite database in the project folder
DB_PATH = Path(__file__).parent / "shopping_analysis.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()

# Create Products Table
cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price REAL NOT NULL
)
""")

# Create Orders Table
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date DATE NOT NULL,
    payment_method TEXT NOT NULL,
    order_status TEXT NOT NULL
        CHECK(order_status IN
        ('Completed', 'Pending', 'Cancelled', 'Refunded'))
)
""")

# Create Order Items Table
cur.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
""")

# Insert Sample Products
cur.execute("SELECT COUNT(*) FROM products")

if cur.fetchone()[0] == 0:
    products = [
        ("Wireless Mouse", "Electronics", 599.00),
        ("USB-C Cable", "Electronics", 249.00),
        ("Notebook", "Stationery", 99.00),
        ("Water Bottle", "Home", 399.00),
        ("Backpack", "Accessories", 1299.00),
        ("Bluetooth Speaker", "Electronics", 1899.00),
        ("Desk Lamp", "Home", 799.00),
        ("Pen Set", "Stationery", 149.00),
    ]

    cur.executemany("""
        INSERT INTO products(product_name, category, unit_price)
        VALUES (?, ?, ?)
    """, products)

# Insert Sample Orders
cur.execute("SELECT COUNT(*) FROM orders")

if cur.fetchone()[0] == 0:
    orders = [
        ("2026-01-03", "UPI", "Completed"),
        ("2026-01-08", "Credit Card", "Completed"),
        ("2026-01-15", "Cash on Delivery", "Cancelled"),
        ("2026-01-22", "Debit Card", "Completed"),
        ("2026-02-02", "UPI", "Completed"),
        ("2026-02-09", "Net Banking", "Pending"),
        ("2026-02-17", "Credit Card", "Refunded"),
        ("2026-02-25", "UPI", "Completed"),
        ("2026-03-04", "Debit Card", "Completed"),
        ("2026-03-11", "Cash on Delivery", "Completed"),
        ("2026-03-19", "UPI", "Pending"),
        ("2026-03-27", "Credit Card", "Completed"),
        ("2026-04-05", "UPI", "Completed"),
        ("2026-04-12", "Net Banking", "Completed"),
        ("2026-04-21", "Debit Card", "Cancelled"),
        ("2026-05-02", "Credit Card", "Completed"),
        ("2026-05-14", "UPI", "Completed"),
        ("2026-05-26", "Cash on Delivery", "Refunded"),
    ]

    cur.executemany("""
        INSERT INTO orders(order_date, payment_method, order_status)
        VALUES (?, ?, ?)
    """, orders)

# Insert Sample Order Items
cur.execute("SELECT COUNT(*) FROM order_items")

if cur.fetchone()[0] == 0:

    cur.execute("SELECT order_id FROM orders ORDER BY order_id")
    order_ids = [row[0] for row in cur.fetchall()]

    rows = []

    for i, oid in enumerate(order_ids):
        p1 = (i % 8) + 1
        p2 = ((i + 3) % 8) + 1

        q1 = (i % 3) + 1
        q2 = (i % 2) + 1

        rows.extend([
            (oid, p1, q1),
            (oid, p2, q2)
        ])

    cur.execute("SELECT product_id, unit_price FROM products")
    prices = {
        pid: price for pid, price in cur.fetchall()
    }

    rows = [
        (oid, pid, qty, prices[pid])
        for oid, pid, qty in rows
    ]

    cur.executemany("""
        INSERT INTO order_items
        (order_id, product_id, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, rows)

# Save database
conn.commit()

print("SQLite database created successfully!")
print("Database location:", DB_PATH)
print("Products:", cur.execute("SELECT COUNT(*) FROM products").fetchone()[0])
print("Orders:", cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
print("Order Items:", cur.execute("SELECT COUNT(*) FROM order_items").fetchone()[0])

cur.close()
conn.close()

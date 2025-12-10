#!/usr/bin/env python3
"""
Prompt: Ingest the generated ecommerce data into a SQLite database.

Create a well-structured relational database with proper:
- Table schemas with appropriate data types
- Primary and foreign key constraints
- Indexes for performance
- Data validation and integrity

Tables to create:
- categories (id, name, description)
- customers (id, name, email, phone, address, registration_date)
- products (id, name, category_id, price, stock_quantity, description)
- orders (id, customer_id, order_date, total_amount, status)
- order_items (id, order_id, product_id, quantity, unit_price)
"""

import sqlite3
import json
from datetime import datetime

def create_database_schema(cursor):
    """Create database tables with proper schema"""
    
    # Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT
        )
    """)
    
    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(50),
            address TEXT,
            registration_date DATE NOT NULL
        )
    """)
    
    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            category_id INTEGER NOT NULL,
            price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
            stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
            description TEXT,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    
    # Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
            status VARCHAR(50) NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    
    # Order items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price >= 0),
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

def create_indexes(cursor):
    """Create indexes for better query performance"""
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)",
        "CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_date)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)",
        "CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id)",
        "CREATE INDEX IF NOT EXISTS idx_customers_email ON customers(email)"
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)

def insert_data(cursor, data):
    """Insert data into database tables"""
    
    # Insert categories
    for category in data["categories"]:
        cursor.execute("""
            INSERT OR REPLACE INTO categories (id, name, description)
            VALUES (?, ?, ?)
        """, (category["id"], category["name"], category["description"]))
    
    # Insert customers
    for customer in data["customers"]:
        cursor.execute("""
            INSERT OR REPLACE INTO customers (id, name, email, phone, address, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer["id"], customer["name"], customer["email"],
            customer["phone"], customer["address"], customer["registration_date"]
        ))
    
    # Insert products
    for product in data["products"]:
        cursor.execute("""
            INSERT OR REPLACE INTO products (id, name, category_id, price, stock_quantity, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product["id"], product["name"], product["category_id"],
            product["price"], product["stock_quantity"], product["description"]
        ))
    
    # Insert orders
    for order in data["orders"]:
        cursor.execute("""
            INSERT OR REPLACE INTO orders (id, customer_id, order_date, total_amount, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order["id"], order["customer_id"], order["order_date"],
            order["total_amount"], order["status"]
        ))
    
    # Insert order items
    for item in data["order_items"]:
        cursor.execute("""
            INSERT OR REPLACE INTO order_items (id, order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            item["id"], item["order_id"], item["product_id"],
            item["quantity"], item["unit_price"]
        ))

def verify_data_integrity(cursor):
    """Verify data was inserted correctly"""
    
    tables = ["categories", "customers", "products", "orders", "order_items"]
    
    print("\nData verification:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"- {table}: {count} records")
    
    # Check foreign key integrity
    cursor.execute("""
        SELECT COUNT(*) FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE c.id IS NULL
    """)
    orphaned_products = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders o
        LEFT JOIN customers c ON o.customer_id = c.id
        WHERE c.id IS NULL
    """)
    orphaned_orders = cursor.fetchone()[0]
    
    print(f"\nData integrity check:")
    print(f"- Orphaned products: {orphaned_products}")
    print(f"- Orphaned orders: {orphaned_orders}")

def main():
    """Main function to create database and ingest data"""
    
    # Load the generated data
    try:
        with open("ecommerce_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: ecommerce_data.json not found. Please run generate_ecommerce_data.py first.")
        return
    
    # Connect to SQLite database
    conn = sqlite3.connect("ecommerce.db")
    cursor = conn.cursor()
    
    try:
        print("Creating database schema...")
        create_database_schema(cursor)
        
        print("Creating indexes...")
        create_indexes(cursor)
        
        print("Inserting data...")
        insert_data(cursor, data)
        
        # Commit changes
        conn.commit()
        
        print("Data ingestion completed successfully!")
        
        # Verify data
        verify_data_integrity(cursor)
        
    except Exception as e:
        print(f"Error during data ingestion: {e}")
        conn.rollback()
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Prompt: Generate synthetic ecommerce data for a multi-table database system.

Create realistic ecommerce data including:
- Customers (id, name, email, phone, address, registration_date)
- Products (id, name, category, price, stock_quantity, description)
- Orders (id, customer_id, order_date, total_amount, status)
- Order_Items (id, order_id, product_id, quantity, unit_price)
- Categories (id, name, description)

Generate approximately 100 customers, 50 products across 10 categories, 
200 orders, and corresponding order items with realistic relationships.
"""

import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_categories():
    """Generate product categories"""
    categories = [
        {"id": 1, "name": "Electronics", "description": "Electronic devices and gadgets"},
        {"id": 2, "name": "Clothing", "description": "Fashion and apparel"},
        {"id": 3, "name": "Books", "description": "Books and literature"},
        {"id": 4, "name": "Home & Garden", "description": "Home improvement and gardening"},
        {"id": 5, "name": "Sports", "description": "Sports and fitness equipment"},
        {"id": 6, "name": "Beauty", "description": "Beauty and personal care"},
        {"id": 7, "name": "Toys", "description": "Toys and games"},
        {"id": 8, "name": "Automotive", "description": "Car parts and accessories"},
        {"id": 9, "name": "Food", "description": "Food and beverages"},
        {"id": 10, "name": "Health", "description": "Health and wellness products"}
    ]
    return categories

def generate_customers(count=100):
    """Generate synthetic customer data"""
    customers = []
    for i in range(1, count + 1):
        customer = {
            "id": i,
            "name": fake.name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace('\n', ', '),
            "registration_date": fake.date_between(start_date='-2y', end_date='today').isoformat()
        }
        customers.append(customer)
    return customers

def generate_products(categories, count=50):
    """Generate synthetic product data"""
    products = []
    product_names = {
        1: ["Smartphone", "Laptop", "Tablet", "Headphones", "Smart Watch"],
        2: ["T-Shirt", "Jeans", "Dress", "Sneakers", "Jacket"],
        3: ["Novel", "Cookbook", "Biography", "Textbook", "Magazine"],
        4: ["Garden Tools", "Furniture", "Lighting", "Decor", "Plants"],
        5: ["Running Shoes", "Yoga Mat", "Dumbbells", "Tennis Racket", "Bicycle"],
        6: ["Skincare Set", "Makeup Kit", "Perfume", "Hair Care", "Nail Polish"],
        7: ["Board Game", "Action Figure", "Puzzle", "Doll", "Building Blocks"],
        8: ["Car Battery", "Oil Filter", "Tire", "Car Cover", "GPS Navigator"],
        9: ["Organic Coffee", "Protein Bar", "Olive Oil", "Spices", "Tea"],
        10: ["Vitamins", "First Aid Kit", "Thermometer", "Supplements", "Fitness Tracker"]
    }
    
    for i in range(1, count + 1):
        category_id = random.randint(1, 10)
        category_products = product_names[category_id]
        
        product = {
            "id": i,
            "name": random.choice(category_products),
            "category_id": category_id,
            "price": round(random.uniform(10.0, 500.0), 2),
            "stock_quantity": random.randint(0, 100),
            "description": fake.text(max_nb_chars=200)
        }
        products.append(product)
    return products

def generate_orders(customers, count=200):
    """Generate synthetic order data"""
    orders = []
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    
    for i in range(1, count + 1):
        order_date = fake.date_between(start_date='-1y', end_date='today')
        order = {
            "id": i,
            "customer_id": random.choice(customers)["id"],
            "order_date": order_date.isoformat(),
            "total_amount": 0,  # Will be calculated after order items
            "status": random.choice(statuses)
        }
        orders.append(order)
    return orders

def generate_order_items(orders, products):
    """Generate synthetic order items data"""
    order_items = []
    item_id = 1
    
    for order in orders:
        # Each order has 1-5 items
        num_items = random.randint(1, 5)
        order_total = 0
        
        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            unit_price = product["price"]
            
            order_item = {
                "id": item_id,
                "order_id": order["id"],
                "product_id": product["id"],
                "quantity": quantity,
                "unit_price": unit_price
            }
            order_items.append(order_item)
            order_total += quantity * unit_price
            item_id += 1
        
        # Update order total
        order["total_amount"] = round(order_total, 2)
    
    return order_items

def main():
    """Generate all ecommerce data"""
    print("Generating synthetic ecommerce data...")
    
    # Generate data
    categories = generate_categories()
    customers = generate_customers(100)
    products = generate_products(categories, 50)
    orders = generate_orders(customers, 200)
    order_items = generate_order_items(orders, products)
    
    # Save to JSON files
    data = {
        "categories": categories,
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }
    
    with open("ecommerce_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Generated:")
    print(f"- {len(categories)} categories")
    print(f"- {len(customers)} customers")
    print(f"- {len(products)} products")
    print(f"- {len(orders)} orders")
    print(f"- {len(order_items)} order items")
    print("Data saved to ecommerce_data.json")

if __name__ == "__main__":
    main()
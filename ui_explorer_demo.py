#!/usr/bin/env python3
"""
UI Explorer Demo - Showcase the beginner-friendly interface
Demonstrates how non-technical users can work with databases
"""

from everything_db import SQLiteDatabase
import os

def main():
    print("SQLite Database Manager - UI Explorer Demo")
    print("=" * 55)
    print("This demo shows how the UI Explorer makes database")
    print("management accessible to everyone!")
    
    # Create demo database
    print("\n1. Creating demo database for UI Explorer...")
    db = SQLiteDatabase("ui_explorer_demo")
    metadata = {
        "description": "UI Explorer demonstration database",
        "purpose": "Showcase beginner-friendly interface",
        "owner": "Demo Script",
        "tags": ["demo", "ui-explorer", "beginner-friendly"]
    }
    db.create_sqlite_db(metadata)
    print("✓ Database 'ui_explorer_demo' created")
    
    # Simulate creating storage spaces through UI Explorer
    print("\n2. Creating storage spaces (like UI Explorer would)...")
    
    # Create customers "storage space"
    print("   Creating 'customers' storage space...")
    customers_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age REAL,
        is_active INTEGER DEFAULT 1,
        signup_date TEXT DEFAULT CURRENT_TIMESTAMP
    """
    db.create_table_safe("customers", customers_schema)
    print("   ✓ Customers storage created")
    
    # Create products "storage space"
    print("   Creating 'products' storage space...")
    products_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        in_stock INTEGER DEFAULT 1,
        category TEXT,
        description TEXT
    """
    db.create_table_safe("products", products_schema)
    print("   ✓ Products storage created")
    
    # Create orders "storage space"
    print("   Creating 'orders' storage space...")
    orders_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id REAL NOT NULL,
        product_id REAL NOT NULL,
        quantity REAL DEFAULT 1,
        order_date TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'pending'
    """
    db.create_table_safe("orders", orders_schema)
    print("   ✓ Orders storage created")
    
    # Add sample data
    print("\n3. Adding sample information...")
    
    # Add customers
    sample_customers = [
        {"name": "Alice Johnson", "email": "alice@email.com", "age": 28},
        {"name": "Bob Smith", "email": "bob@email.com", "age": 35}, 
        {"name": "Carol Davis", "email": "carol@email.com", "age": 42},
        {"name": "David Wilson", "email": "david@email.com", "age": 31},
        {"name": "Eva Brown", "email": "eva@email.com", "age": 29}
    ]
    
    for customer in sample_customers:
        db.insert_data("customers", customer)
    print("   ✓ Added customer information")
    
    # Add products
    sample_products = [
        {"product_name": "Laptop", "price": 999.99, "category": "Electronics", "description": "High-performance laptop"},
        {"product_name": "Coffee Mug", "price": 12.99, "category": "Kitchen", "description": "Ceramic coffee mug"},
        {"product_name": "Notebook", "price": 5.99, "category": "Office", "description": "Spiral-bound notebook"},
        {"product_name": "Headphones", "price": 79.99, "category": "Electronics", "description": "Wireless headphones"},
        {"product_name": "Plant Pot", "price": 18.50, "category": "Garden", "description": "Ceramic plant pot"}
    ]
    
    for product in sample_products:
        db.insert_data("products", product)
    print("   ✓ Added product information")
    
    # Add orders
    sample_orders = [
        {"customer_id": 1, "product_id": 1, "quantity": 1, "status": "completed"},
        {"customer_id": 2, "product_id": 3, "quantity": 2, "status": "pending"},
        {"customer_id": 1, "product_id": 4, "quantity": 1, "status": "shipped"},
        {"customer_id": 3, "product_id": 2, "quantity": 3, "status": "completed"},
        {"customer_id": 4, "product_id": 5, "quantity": 1, "status": "pending"}
    ]
    
    for order in sample_orders:
        db.insert_data("orders", order)
    print("   ✓ Added order information")
    
    # Demonstrate UI Explorer concepts
    print("\n4. Demonstrating UI Explorer concepts...")
    
    print("\n📊 DATA OVERVIEW (as UI Explorer would show):")
    print("-" * 50)
    
    tables = db.get_tables()
    for table in tables:
        count = db.select_count_from_sqlite_table(table, "1=1")
        columns = db.get_column_info(table)
        
        print(f"\n📁 Storage Space: {table}")
        print(f"   Items stored: {count}")
        print(f"   Information fields: {len(columns)}")
        
        # Show field names in friendly way
        field_names = []
        for col in columns:
            cid, name, data_type, not_null, default_val, is_pk = col
            type_friendly = {
                'INTEGER': 'Numbers',
                'TEXT': 'Text/Words', 
                'REAL': 'Decimal Numbers'
            }.get(data_type, data_type)
            
            if is_pk:
                field_names.append(f"{name} (ID)")
            else:
                field_names.append(f"{name} ({type_friendly})")
        
        print(f"   Fields: {', '.join(field_names)}")
    
    # Show sample search
    print("\n🔍 SAMPLE SEARCH (finding customers named 'Alice'):")
    print("-" * 50)
    alice_results = db.execute_query("SELECT * FROM customers WHERE name LIKE '%Alice%'")
    if alice_results:
        print("Found matching customers:")
        for row in alice_results:
            print(f"   ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Age: {row[3]}")
    
    # Show data relationships
    print("\n🔗 DATA RELATIONSHIPS (orders with customer names):")
    print("-" * 50)
    order_details = db.execute_query("""
        SELECT o.id, c.name, p.product_name, o.quantity, o.status
        FROM orders o, customers c, products p 
        WHERE o.customer_id = c.id AND o.product_id = p.id
        LIMIT 3
    """)
    
    if order_details:
        print("Recent orders:")
        for order in order_details:
            print(f"   Order #{order[0]}: {order[1]} bought {order[2]} (qty: {order[3]}) - {order[4]}")
    
    print("\n" + "=" * 55)
    print("UI Explorer Demo Features Demonstrated:")
    print("✓ User-friendly terminology ('storage space' vs 'table')")
    print("✓ Plain language data types ('Text/Words' vs 'TEXT')")
    print("✓ Intuitive data browsing and summaries")
    print("✓ Simple search without SQL knowledge")
    print("✓ Clear field descriptions and requirements")
    print("✓ Automatic ID field management")
    print()
    print("🎯 The UI Explorer makes database management accessible")
    print("   to users without technical database knowledge!")
    print()
    print("Try it yourself:")
    print("   uv run everything_ui.py")
    print("   Choose option 10: 'UI Explorer (Beginner-Friendly)'")

if __name__ == "__main__":
    main()
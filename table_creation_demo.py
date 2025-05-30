#!/usr/bin/env python3
"""
Demo script showing table creation features
Demonstrates both interactive and programmatic table creation
"""

from everything_db import SQLiteDatabase


def main():
    print("SQLite Database Manager - Table Creation Demo")
    print("=" * 55)

    # Create a demo database
    print("\n1. Creating demo database...")
    db = SQLiteDatabase("table_demo")
    metadata = {
        "description": "Demonstration of table creation features",
        "purpose": "Educational demo",
        "owner": "Demo Script",
        "tags": ["demo", "tables", "tutorial"],
    }
    db.create_sqlite_db(metadata)
    print("✓ Database 'table_demo' created")

    # Demo 1: Create a users table
    print("\n2. Creating 'users' table...")
    users_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        full_name TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    """

    try:
        db.create_table_safe("users", users_schema)
        print("✓ Users table created successfully")
    except Exception as e:
        print(f"✗ Error creating users table: {e}")

    # Demo 2: Create a products table
    print("\n3. Creating 'products' table...")
    products_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL CHECK(price >= 0),
        stock_quantity INTEGER DEFAULT 0,
        category_id INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    """

    try:
        db.create_table_safe("products", products_schema)
        print("✓ Products table created successfully")
    except Exception as e:
        print(f"✗ Error creating products table: {e}")

    # Demo 3: Create a categories table
    print("\n4. Creating 'categories' table...")
    categories_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES categories(id)
    """

    try:
        db.create_table_safe("categories", categories_schema)
        print("✓ Categories table created successfully")
    except Exception as e:
        print(f"✗ Error creating categories table: {e}")

    # Demo 4: Create an orders table with complex constraints
    print("\n5. Creating 'orders' table with complex constraints...")
    orders_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount REAL NOT NULL CHECK(total_amount > 0),
        status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
        order_date TEXT DEFAULT CURRENT_TIMESTAMP,
        shipping_address TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    """

    try:
        db.create_table_safe("orders", orders_schema)
        print("✓ Orders table created successfully")
    except Exception as e:
        print(f"✗ Error creating orders table: {e}")

    # Demo 5: Try to create a table with invalid name (should fail)
    print("\n6. Testing invalid table name...")
    try:
        db.create_table_safe("select", "id INTEGER PRIMARY KEY")
        print("✗ Should have failed - reserved keyword allowed")
    except Exception as e:
        print(f"✓ Correctly rejected reserved keyword: {e}")

    # Demo 6: Try to create duplicate table (should fail)
    print("\n7. Testing duplicate table creation...")
    try:
        db.create_table_safe("users", "id INTEGER PRIMARY KEY")
        print("✗ Should have failed - duplicate table allowed")
    except Exception as e:
        print(f"✓ Correctly rejected duplicate table: {e}")

    # Demo 7: Show all tables created
    print("\n8. Listing all tables...")
    tables = db.get_tables()
    print(f"✓ Created {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")

    # Demo 8: Show detailed schema for each table
    print("\n9. Table schemas:")
    for table in tables:
        print(f"\n--- {table.upper()} TABLE ---")
        columns = db.get_column_info(table)
        for col in columns:
            cid, name, data_type, not_null, default_val, is_pk = col
            pk_marker = " (PRIMARY KEY)" if is_pk else ""
            null_marker = " NOT NULL" if not_null else ""
            default_marker = f" DEFAULT {default_val}" if default_val else ""
            print(f"  {name}: {data_type}{pk_marker}{null_marker}{default_marker}")

    # Demo 9: Insert sample data
    print("\n10. Inserting sample data...")

    # Insert categories
    sample_categories = [
        {"name": "Electronics", "description": "Electronic devices and gadgets"},
        {"name": "Books", "description": "Physical and digital books"},
        {"name": "Clothing", "description": "Apparel and accessories"},
    ]

    for category in sample_categories:
        db.insert_data("categories", category)
    print("✓ Sample categories inserted")

    # Insert users
    sample_users = [
        {"username": "john_doe", "email": "john@example.com", "full_name": "John Doe"},
        {
            "username": "jane_smith",
            "email": "jane@example.com",
            "full_name": "Jane Smith",
        },
        {
            "username": "bob_wilson",
            "email": "bob@example.com",
            "full_name": "Bob Wilson",
        },
    ]

    for user in sample_users:
        db.insert_data("users", user)
    print("✓ Sample users inserted")

    # Insert products
    sample_products = [
        {
            "name": "Laptop",
            "description": "High-performance laptop",
            "price": 999.99,
            "stock_quantity": 10,
            "category_id": 1,
        },
        {
            "name": "Python Book",
            "description": "Learn Python programming",
            "price": 29.99,
            "stock_quantity": 50,
            "category_id": 2,
        },
        {
            "name": "T-Shirt",
            "description": "Cotton t-shirt",
            "price": 19.99,
            "stock_quantity": 100,
            "category_id": 3,
        },
    ]

    for product in sample_products:
        db.insert_data("products", product)
    print("✓ Sample products inserted")

    # Demo 10: Show table data
    print("\n11. Sample data in tables:")

    print("\nCategories:")
    categories = db.get_table_data("categories", 5)
    for cat in categories:
        print(f"  {cat[0]}: {cat[1]} - {cat[2]}")

    print("\nUsers:")
    users = db.get_table_data("users", 5)
    for user in users:
        print(f"  {user[0]}: {user[1]} ({user[2]}) - {user[3]}")

    print("\nProducts:")
    products = db.get_table_data("products", 5)
    for product in products:
        print(f"  {product[0]}: {product[1]} - ${product[3]} (Stock: {product[4]})")

    print("\n" + "=" * 55)
    print("Table creation demo completed!")
    print("You can now run 'uv run everything_ui.py' to interact with this database.")
    print("Use option 4 'Create Table' to try the interactive table creation.")


if __name__ == "__main__":
    main()

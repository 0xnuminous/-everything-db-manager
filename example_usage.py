#!/usr/bin/env python3
"""
Example usage of the SQLite Database Manager
Demonstrates creating databases, tables, and basic operations
"""

from everything_db import SQLiteDatabase


def main():
    print("SQLite Database Manager - Example Usage")
    print("=" * 50)

    # Example 1: Create a new database with metadata
    print("\n1. Creating a new database with metadata...")

    db = SQLiteDatabase("example_store")
    metadata = {
        "description": "Example e-commerce store database",
        "purpose": "Demonstration and testing",
        "owner": "Development Team",
        "tags": ["example", "ecommerce", "demo"],
    }

    db.create_sqlite_db(metadata)
    print(f"✓ Created database: {db.db_name}")

    # Example 2: Create tables
    print("\n2. Creating tables...")

    # Products table
    products_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        category TEXT,
        created_date TEXT DEFAULT CURRENT_TIMESTAMP
    """

    db.create_sqlite_table("products", products_schema)
    print("✓ Created products table")

    # Categories table
    categories_schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    """

    db.create_sqlite_table("categories", categories_schema)
    print("✓ Created categories table")

    # Example 3: Insert sample data
    print("\n3. Inserting sample data...")

    # Insert categories
    categories_data = [
        {"name": "Electronics", "description": "Electronic devices and accessories"},
        {"name": "Books", "description": "Physical and digital books"},
        {"name": "Clothing", "description": "Apparel and accessories"},
    ]

    for category in categories_data:
        db.insert_data("categories", category)

    print("✓ Inserted category data")

    # Insert products
    products_data = [
        {
            "name": "Wireless Headphones",
            "description": "High-quality bluetooth headphones",
            "price": 79.99,
            "stock_quantity": 25,
            "category": "Electronics",
        },
        {
            "name": "Python Programming Book",
            "description": "Learn Python from basics to advanced",
            "price": 34.99,
            "stock_quantity": 50,
            "category": "Books",
        },
        {
            "name": "Cotton T-Shirt",
            "description": "Comfortable 100% cotton t-shirt",
            "price": 19.99,
            "stock_quantity": 100,
            "category": "Clothing",
        },
    ]

    for product in products_data:
        db.insert_data("products", product)

    print("✓ Inserted product data")

    # Example 4: Query data
    print("\n4. Querying data...")

    # Get all tables
    tables = db.get_tables()
    print(f"Tables in database: {', '.join(tables)}")

    # Get all products
    products = db.select_all_from_sqlite_table("products")
    print(f"Total products: {len(products)}")

    # Get products with price > 30
    expensive_products = db.execute_query(
        "SELECT name, price FROM products WHERE price > 30"
    )
    print("Products over $30:")
    for product in expensive_products:
        print(f"  - {product[0]}: ${product[1]}")

    # Example 5: Database statistics
    print("\n5. Database statistics...")

    total_products = db.select_count_from_sqlite_table("products", "1=1")
    total_value = db.select_sum_from_sqlite_table(
        "products", "price * stock_quantity", "1=1"
    )

    print(f"Total products: {total_products}")
    print(f"Total inventory value: ${total_value:.2f}")

    # Example 6: Show metadata
    print("\n6. Database metadata...")

    metadata = db.get_metadata()
    if metadata:
        print(f"Description: {metadata.get('description')}")
        print(f"Purpose: {metadata.get('purpose')}")
        print(f"Owner: {metadata.get('owner')}")
        print(f"Tags: {', '.join(metadata.get('tags', []))}")
        print(f"Created: {metadata.get('created_date')}")

    # Example 7: Update data
    print("\n7. Updating data...")

    db.update_sqlite_table(
        "products",
        "stock_quantity = stock_quantity - 1",
        "name = 'Wireless Headphones'",
    )
    print("✓ Updated headphones stock")

    # Example 8: Complex query with JOIN-like operation
    print("\n8. Advanced query...")

    electronics = db.execute_query(
        "SELECT name, price, stock_quantity FROM products WHERE category = 'Electronics'"
    )
    print("Electronics inventory:")
    for item in electronics:
        print(f"  - {item[0]}: ${item[1]} (Stock: {item[2]})")

    print("\n" + "=" * 50)
    print(
        "Example completed! Check the 'data' directory for the created database file."
    )
    print("Metadata is stored internally within the database, not in separate files.")
    print("You can now run 'uv run everything_ui.py' to interact with this database.")


if __name__ == "__main__":
    main()

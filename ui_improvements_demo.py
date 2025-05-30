#!/usr/bin/env python3
"""
Demo script showing UI improvements for table creation and schema display
"""

from everything_db import SQLiteDatabase
import os


def demo_data_type_flexibility():
    """Demo improved data type input handling"""
    print("=== Data Type Flexibility Demo ===")
    print("The system now accepts common abbreviations and variations:")

    type_mapping = {
        "INT": "INTEGER",
        "INTEGER": "INTEGER",
        "STRING": "TEXT",
        "TEXT": "TEXT",
        "VARCHAR": "TEXT",
        "CHAR": "TEXT",
        "FLOAT": "REAL",
        "DOUBLE": "REAL",
        "REAL": "REAL",
        "DECIMAL": "REAL",
        "BLOB": "BLOB",
        "BINARY": "BLOB",
    }

    print("\nAccepted data type inputs:")
    for input_type, mapped_type in type_mapping.items():
        print(f"  '{input_type.lower()}' -> {mapped_type}")

    print("\nInvalid types default to TEXT with helpful message.")


def demo_improved_schema_display():
    """Demo improved schema table display"""
    print("\n=== Improved Schema Display Demo ===")

    # Create test database
    db = SQLiteDatabase("ui_demo")
    db.create_sqlite_db()

    # Create sample table with various constraints
    schema = """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        age INTEGER,
        balance REAL DEFAULT 0.0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    """

    try:
        db.create_table_safe("users", schema)
        print("✓ Created sample 'users' table")

        print("\nOLD Schema Display (raw SQLite data):")
        print("  (0, 'id', 'INTEGER', 0, None, 1)")
        print("  (1, 'username', 'TEXT', 1, None, 0)")
        print("  (2, 'email', 'TEXT', 1, None, 0)")
        print("  ...")

        print("\nNEW Schema Display (formatted table):")
        schema_info = db.get_table_schema("users")
        if schema_info:
            print("-" * 70)
            print(
                f"{'Column':<15} {'Type':<12} {'Nullable':<10} {'Key':<10} {'Default':<15}"
            )
            print("-" * 70)
            for column in schema_info:
                cid, name, data_type, not_null, default_val, is_pk = column
                nullable = "NO" if not_null else "YES"
                key = "PRIMARY" if is_pk else ""
                default = str(default_val) if default_val is not None else ""
                print(
                    f"{name:<15} {data_type:<12} {nullable:<10} {key:<10} {default:<15}"
                )

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        if os.path.exists("data/ui_demo.db"):
            os.remove("data/ui_demo.db")


def demo_table_existence_checks():
    """Demo improved table existence checking and suggestions"""
    print("\n=== Table Existence Checks Demo ===")

    db = SQLiteDatabase("existence_demo")
    db.create_sqlite_db()

    # Create some tables
    db.create_table_safe("products", "id INTEGER PRIMARY KEY, name TEXT")
    db.create_table_safe("categories", "id INTEGER PRIMARY KEY, name TEXT")
    db.create_table_safe("orders", "id INTEGER PRIMARY KEY, total REAL")

    print("✓ Created sample tables: products, categories, orders")

    print("\nWhen user enters invalid table name, system now provides:")
    print("1. Clear error message")
    print("2. List of available tables")
    print("3. Helpful suggestions")

    print("\nExample output for non-existent table 'customer':")
    print("  Table 'customer' not found.")
    print("  Available tables:")
    tables = db.get_tables()
    for i, table in enumerate(tables, 1):
        print(f"    {i}. {table}")

    # Cleanup
    if os.path.exists("data/existence_demo.db"):
        os.remove("data/existence_demo.db")


def demo_improved_data_entry():
    """Demo improved data entry with validation and feedback"""
    print("\n=== Improved Data Entry Demo ===")

    print("Data entry improvements:")
    print("1. Shows example format")
    print("2. Warns about duplicate column names")
    print("3. Handles quoted values properly")
    print("4. Provides real-time feedback")

    print("\nExample session:")
    print(
        "Enter column=value pairs (one per line, press Enter on empty line to finish):"
    )
    print("Example: name=John Doe, age=25, email=john@example.com")
    print()
    print("name=John Doe")
    print("  Added: name = John Doe")
    print('email="john@example.com"')
    print("  Added: email = john@example.com")
    print("name=Jane Smith")
    print("  Warning: Column 'name' already specified. Overwriting previous value.")
    print("  Added: name = Jane Smith")


def main():
    print("SQLite Database Manager - UI Improvements Demo")
    print("=" * 60)

    demo_data_type_flexibility()
    demo_improved_schema_display()
    demo_table_existence_checks()
    demo_improved_data_entry()

    print("\n" + "=" * 60)
    print("UI Improvements Summary:")
    print("✓ Flexible data type input (int, string, float, etc.)")
    print("✓ Beautiful formatted schema display")
    print("✓ Table existence validation with suggestions")
    print("✓ Enhanced data entry with real-time feedback")
    print("✓ Better error messages and user guidance")
    print("\nThese improvements make the system much more user-friendly!")


if __name__ == "__main__":
    main()

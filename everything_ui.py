from everything_db import SQLiteDatabase
import sys


class DatabaseTerminalUI:
    def __init__(self):
        self.db = None
        self.current_db_path = None
        self.current_db_name = None

    def display_menu(self):
        print("\n" + "=" * 50)
        print("         SQLite Database Manager")
        print("=" * 50)
        print("1. Open/Create Database")
        print("2. List All Databases")
        print("3. List Tables")
        print("4. Create Table")
        print("5. Execute Query")
        print("6. Show Table Schema")
        print("7. Insert Data")
        print("8. View Table Data")
        print("9. Show Database Info")
        print("10. Close Database")
        print("11. Exit")
        print("-" * 50)

    def get_user_choice(self):
        try:
            choice = input("Enter your choice (1-11): ").strip()
            return int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 11.")
            return None

    def open_database(self):
        print("\nDatabase Options:")
        print("1. Create new database")
        print("2. Open existing database")

        choice = input("Enter choice (1-2): ").strip()

        if choice == "1":
            self._create_new_database()
        elif choice == "2":
            self._open_existing_database()
        else:
            print("Invalid choice.")

    def _create_new_database(self):
        db_name = input("Enter database name (without .db extension): ").strip()
        if not db_name:
            print("Database name cannot be empty.")
            return

        print("\nDatabase Metadata:")
        description = input("Description: ").strip()
        purpose = input("Purpose/Project: ").strip()
        owner = input("Owner/Creator: ").strip()
        tags = input("Tags (comma-separated): ").strip()

        metadata = {
            "description": description,
            "purpose": purpose,
            "owner": owner,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
        }

        try:
            self.db = SQLiteDatabase(db_name)
            self.db.create_sqlite_db(metadata)
            self.current_db_path = self.db.db_name
            self.current_db_name = db_name
            print(f"Successfully created database: {db_name}")
        except Exception as e:
            print(f"Error creating database: {e}")

    def _open_existing_database(self):
        # Show available databases
        temp_db = SQLiteDatabase("temp")  # Just to access list_all_databases
        databases = temp_db.list_all_databases()

        if not databases:
            print("No databases found in data directory.")
            return

        print("\nAvailable databases:")
        for i, db_info in enumerate(databases, 1):
            metadata = db_info.get("metadata", {})
            description = (
                metadata.get("description", "No description")
                if metadata
                else "No description"
            )
            print(f"{i}. {db_info['name']} - {description}")

        try:
            choice = int(input("Enter database number: ").strip())
            if 1 <= choice <= len(databases):
                selected_db = databases[choice - 1]
                self.db = SQLiteDatabase(selected_db["name"])
                self.current_db_path = selected_db["path"]
                self.current_db_name = selected_db["name"]
                print(f"Successfully opened database: {selected_db['name']}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"Error opening database: {e}")

    def list_all_databases(self):
        try:
            temp_db = SQLiteDatabase("temp")  # Just to access list_all_databases
            databases = temp_db.list_all_databases()

            if not databases:
                print("No databases found in data directory.")
                return

            print("\n" + "=" * 60)
            print("                    ALL DATABASES")
            print("=" * 60)

            for db_info in databases:
                metadata = db_info.get("metadata", {})
                print(f"\nDatabase: {db_info['name']}")
                print(f"File: {db_info['file']}")

                if metadata:
                    print(f"Description: {metadata.get('description', 'N/A')}")
                    print(f"Purpose: {metadata.get('purpose', 'N/A')}")
                    print(f"Owner: {metadata.get('owner', 'N/A')}")
                    print(f"Created: {metadata.get('created_date', 'N/A')}")
                    print(f"Last Modified: {metadata.get('last_modified', 'N/A')}")
                    if metadata.get("tags"):
                        print(f"Tags: {', '.join(metadata['tags'])}")
                else:
                    print("No metadata available")
                print("-" * 40)

        except Exception as e:
            print(f"Error listing databases: {e}")

    def create_table(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        print("\nTable Creation Options:")
        print("1. Interactive table creation (guided)")
        print("2. Manual SQL definition")

        choice = input("Enter choice (1-2): ").strip()

        if choice == "1":
            self._create_table_interactive()
        elif choice == "2":
            self._create_table_manual()
        else:
            print("Invalid choice.")

    def _create_table_interactive(self):
        table_name = input("Enter table name: ").strip()
        if not table_name:
            print("Table name cannot be empty.")
            return

        print(f"\nDefining columns for table '{table_name}':")
        print("Enter column definitions (press Enter on empty name to finish)")
        print("Available types: INTEGER, TEXT, REAL, BLOB")
        print("Constraints: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT value")

        columns = []
        while True:
            print(f"\nColumn {len(columns) + 1}:")
            col_name = input("  Column name (or Enter to finish): ").strip()
            if not col_name:
                break

            col_type = input("  Data type (INTEGER/TEXT/REAL/BLOB): ").strip().upper()

            # Handle common abbreviations and variations
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

            if col_type in type_mapping:
                col_type = type_mapping[col_type]
            else:
                print(f"  Invalid data type '{col_type}'. Using TEXT as default.")
                print(
                    "  Valid types: INTEGER (or INT), TEXT (or STRING), REAL (or FLOAT), BLOB"
                )
                col_type = "TEXT"

            constraints = []

            # Check for primary key
            if input("  Primary key? (y/n): ").strip().lower() == "y":
                constraints.append("PRIMARY KEY")
                if col_type == "INTEGER":
                    auto_inc = input("  Auto increment? (y/n): ").strip().lower()
                    if auto_inc == "y":
                        constraints.append("AUTOINCREMENT")

            # Check for not null
            if input("  Not null? (y/n): ").strip().lower() == "y":
                constraints.append("NOT NULL")

            # Check for unique
            if input("  Unique? (y/n): ").strip().lower() == "y":
                constraints.append("UNIQUE")

            # Check for default value
            default_val = input("  Default value (or Enter for none): ").strip()
            if default_val:
                if col_type in ["TEXT"]:
                    constraints.append(f"DEFAULT '{default_val}'")
                else:
                    constraints.append(f"DEFAULT {default_val}")

            # Build column definition
            column_def = f"{col_name} {col_type}"
            if constraints:
                column_def += " " + " ".join(constraints)

            columns.append(column_def)
            print(f"  Added: {column_def}")

        if not columns:
            print("No columns defined. Table creation cancelled.")
            return

        # Show final table definition
        columns_sql = ",\n    ".join(columns)
        full_sql = f"CREATE TABLE {table_name} (\n    {columns_sql}\n)"

        print("\nFinal table definition:")
        print(full_sql)

        confirm = input("\nCreate this table? (y/n): ").strip().lower()
        if confirm == "y":
            try:
                self.db.create_table_safe(table_name, columns_sql)
                print(f"✓ Table '{table_name}' created successfully!")
            except Exception as e:
                print(f"Error creating table: {e}")
        else:
            print("Table creation cancelled.")

    def _create_table_manual(self):
        table_name = input("Enter table name: ").strip()
        if not table_name:
            print("Table name cannot be empty.")
            return

        print(f"\nEnter column definitions for table '{table_name}':")
        print("Example: id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER")
        print("Press Enter twice when finished:")

        column_lines = []
        while True:
            line = input().strip()
            if line == "" and column_lines:
                break
            if line:
                column_lines.append(line)

        if not column_lines:
            print("No column definitions provided. Table creation cancelled.")
            return

        columns_sql = " ".join(column_lines)

        # Show final table definition
        full_sql = f"CREATE TABLE {table_name} ({columns_sql})"
        print("\nTable definition:")
        print(full_sql)

        confirm = input("\nCreate this table? (y/n): ").strip().lower()
        if confirm == "y":
            try:
                self.db.create_table_safe(table_name, columns_sql)
                print(f"✓ Table '{table_name}' created successfully!")
            except Exception as e:
                print(f"Error creating table: {e}")
        else:
            print("Table creation cancelled.")

    def list_tables(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        try:
            tables = self.db.get_tables()
            if tables:
                print("\nTables in database:")
                for i, table in enumerate(tables, 1):
                    print(f"{i}. {table}")
            else:
                print("No tables found in database.")
        except Exception as e:
            print(f"Error listing tables: {e}")

    def execute_query(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        print("Enter SQL query (press Enter twice to execute):")
        query_lines = []
        while True:
            line = input()
            if line == "" and query_lines:
                break
            query_lines.append(line)

        query = "\n".join(query_lines).strip()
        if not query:
            print("No query entered.")
            return

        try:
            result = self.db.execute_query(query)
            if result:
                print("\nQuery Results:")
                for row in result:
                    print(row)
            else:
                print("Query executed successfully (no results returned).")
        except Exception as e:
            print(f"Error executing query: {e}")

    def show_table_schema(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        table_name = input("Enter table name: ").strip()
        try:
            schema = self.db.get_table_schema(table_name)
            if schema:
                print(f"\nSchema for table '{table_name}':")
                print("-" * 60)
                print(
                    f"{'Column':<20} {'Type':<15} {'Nullable':<10} {'Key':<10} {'Default'}"
                )
                print("-" * 60)
                for column in schema:
                    cid, name, data_type, not_null, default_val, is_pk = column
                    nullable = "NO" if not_null else "YES"
                    key = "PRIMARY" if is_pk else ""
                    default = str(default_val) if default_val is not None else ""
                    print(
                        f"{name:<20} {data_type:<15} {nullable:<10} {key:<10} {default}"
                    )
            else:
                print(f"Table '{table_name}' not found.")
                tables = self.db.get_tables()
                if tables:
                    print("Available tables:")
                    for i, table in enumerate(tables, 1):
                        print(f"  {i}. {table}")
                else:
                    print(
                        "No tables exist in this database. Use 'Create Table' to add one."
                    )
        except Exception as e:
            print(f"Error getting table schema: {e}")

    def insert_data(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        table_name = input("Enter table name: ").strip()

        # Check if table exists first
        if not self.db.table_exists(table_name):
            print(f"Table '{table_name}' not found.")
            tables = self.db.get_tables()
            if tables:
                print("Available tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table}")
            else:
                print(
                    "No tables exist in this database. Use 'Create Table' to add one."
                )
            return

        print(
            "Enter column=value pairs (one per line, press Enter on empty line to finish):"
        )
        print("Example: name=John Doe, age=25, email=john@example.com")

        data = {}
        while True:
            entry = input().strip()
            if not entry:
                break
            if "=" in entry:
                key, value = entry.split("=", 1)
                column_name = key.strip()
                column_value = value.strip()

                if column_name in data:
                    print(
                        f"Warning: Column '{column_name}' already specified. Overwriting previous value."
                    )

                # Remove quotes if present
                if column_value.startswith('"') and column_value.endswith('"'):
                    column_value = column_value[1:-1]
                elif column_value.startswith("'") and column_value.endswith("'"):
                    column_value = column_value[1:-1]

                data[column_name] = column_value
                print(f"  Added: {column_name} = {column_value}")
            else:
                print("Invalid format. Use: column=value")

        if data:
            try:
                self.db.insert_data(table_name, data)
                print("Data inserted successfully.")
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            print("No data to insert.")

    def view_table_data(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        table_name = input("Enter table name: ").strip()

        # Check if table exists first
        if not self.db.table_exists(table_name):
            print(f"Table '{table_name}' not found.")
            tables = self.db.get_tables()
            if tables:
                print("Available tables:")
                for i, table in enumerate(tables, 1):
                    print(f"  {i}. {table}")
            else:
                print(
                    "No tables exist in this database. Use 'Create Table' to add one."
                )
            return

        limit = input("Enter number of rows to display (default: 10): ").strip()

        try:
            limit = int(limit) if limit else 10
            data = self.db.get_table_data(table_name, limit)

            if data:
                print(f"\nFirst {limit} rows from table '{table_name}':")
                for row in data:
                    print(row)
            else:
                print(f"No data found in table '{table_name}'.")
        except Exception as e:
            print(f"Error viewing table data: {e}")

    def show_database_info(self):
        if not self.db:
            print("No database opened. Please open a database first.")
            return

        try:
            metadata = self.db.get_metadata()
            print("\n" + "=" * 50)
            print("         DATABASE INFORMATION")
            print("=" * 50)
            print(f"Database Name: {self.current_db_name}")
            print(f"File Path: {self.current_db_path}")

            if metadata:
                print(f"Description: {metadata.get('description', 'N/A')}")
                print(f"Purpose: {metadata.get('purpose', 'N/A')}")
                print(f"Owner: {metadata.get('owner', 'N/A')}")
                print(f"Created: {metadata.get('created_date', 'N/A')}")
                print(f"Last Modified: {metadata.get('last_modified', 'N/A')}")
                if metadata.get("tags"):
                    print(f"Tags: {', '.join(metadata['tags'])}")
            else:
                print("No metadata available for this database.")

            # Show table count
            tables = self.db.get_tables()
            print(f"Number of tables: {len(tables)}")
            if tables:
                print(f"Tables: {', '.join(tables)}")

        except Exception as e:
            print(f"Error getting database info: {e}")

    def close_database(self):
        if self.db:
            try:
                self.db.close()
                self.db = None
                self.current_db_path = None
                self.current_db_name = None
                print("Database closed successfully.")
            except Exception as e:
                print(f"Error closing database: {e}")
        else:
            print("No database is currently open.")

    def run(self):
        print("Welcome to SQLite Database Manager!")

        while True:
            self.display_menu()
            if self.current_db_name:
                print(f"Current database: {self.current_db_name}")

            choice = self.get_user_choice()

            if choice == 1:
                self.open_database()
            elif choice == 2:
                self.list_all_databases()
            elif choice == 3:
                self.list_tables()
            elif choice == 4:
                self.create_table()
            elif choice == 5:
                self.execute_query()
            elif choice == 6:
                self.show_table_schema()
            elif choice == 7:
                self.insert_data()
            elif choice == 8:
                self.view_table_data()
            elif choice == 9:
                self.show_database_info()
            elif choice == 10:
                self.close_database()
            elif choice == 11:
                self.close_database()
                print("Thank you for using SQLite Database Manager!")
                sys.exit(0)
            elif choice is not None:
                print("Invalid choice. Please select a number between 1 and 11.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    ui = DatabaseTerminalUI()
    ui.run()

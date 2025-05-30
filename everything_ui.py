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
        print("10. UI Explorer (Beginner-Friendly)")
        print("11. Close Database")
        print("12. Exit")
        print("-" * 50)

    def get_user_choice(self):
        try:
            choice = input("Enter your choice (1-12): ").strip()
            return int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 12.")
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

    def ui_explorer(self):
        """Beginner-friendly UI explorer for non-technical users"""
        if not self.db:
            print("No database opened. Please open a database first.")
            return
            
        while True:
            print("\n" + "="*60)
            print("         🔍 UI EXPLORER - Beginner Friendly")
            print("="*60)
            print("This explorer helps you work with your data without")
            print("needing to know database terminology!")
            print("-"*60)
            print("1. 📊 Browse My Data (see what's stored)")
            print("2. ➕ Add New Information (create storage space)")
            print("3. ✏️  Update Existing Information")
            print("4. 🔍 Search & Filter Data")
            print("5. 📈 Get Data Summary")
            print("6. ❓ What can I do here? (Help)")
            print("7. 🔙 Back to Main Menu")
            print("-"*60)
            
            try:
                choice = input("What would you like to do? (1-7): ").strip()
                choice_num = int(choice)
                
                if choice_num == 1:
                    self._explorer_browse_data()
                elif choice_num == 2:
                    self._explorer_add_storage()
                elif choice_num == 3:
                    self._explorer_update_data()
                elif choice_num == 4:
                    self._explorer_search_data()
                elif choice_num == 5:
                    self._explorer_data_summary()
                elif choice_num == 6:
                    self._explorer_help()
                elif choice_num == 7:
                    break
                else:
                    print("Please choose a number between 1 and 7.")
                    
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"Something went wrong: {e}")
                
            input("\nPress Enter to continue...")

    def _explorer_browse_data(self):
        """Browse data in user-friendly terms"""
        print("\n📊 BROWSING YOUR DATA")
        print("="*40)
        
        tables = self.db.get_tables()
        if not tables:
            print("💡 You don't have any data storage yet!")
            print("   Use 'Add New Information' to create your first storage space.")
            return
            
        print("Your data is organized in these storage spaces:")
        for i, table in enumerate(tables, 1):
            # Get row count
            try:
                count = self.db.select_count_from_sqlite_table(table, "1=1")
                print(f"{i}. 📁 {table} ({count} items stored)")
            except:
                print(f"{i}. 📁 {table}")
        
        try:
            choice = input("\nWhich storage space would you like to look at? (number): ").strip()
            table_index = int(choice) - 1
            
            if 0 <= table_index < len(tables):
                selected_table = tables[table_index]
                self._explorer_show_table_friendly(selected_table)
            else:
                print("Please choose a valid number from the list.")
        except ValueError:
            print("Please enter a number.")

    def _explorer_show_table_friendly(self, table_name):
        """Show table data in user-friendly format"""
        print(f"\n📁 VIEWING: {table_name}")
        print("="*50)
        
        # Get column info
        columns = self.db.get_column_info(table_name)
        if not columns:
            print("This storage space appears to be empty or has issues.")
            return
            
        # Show what information is stored
        print("This storage space contains these types of information:")
        for col in columns:
            cid, name, data_type, not_null, default_val, is_pk = col
            type_friendly = {
                'INTEGER': 'Numbers',
                'TEXT': 'Text/Words', 
                'REAL': 'Decimal Numbers',
                'BLOB': 'Files/Data'
            }.get(data_type, data_type)
            
            required = " (Required)" if not_null else " (Optional)"
            key_info = " [ID Field]" if is_pk else ""
            
            print(f"  • {name}: {type_friendly}{required}{key_info}")
        
        # Show sample data
        try:
            data = self.db.get_table_data(table_name, 5)
            if data:
                print(f"\nFirst few items stored (showing up to 5):")
                print("-" * 50)
                
                # Create simple display
                col_names = [col[1] for col in columns]
                
                # Header
                header = " | ".join(f"{name[:15]:<15}" for name in col_names)
                print(header)
                print("-" * len(header))
                
                # Data rows
                for row in data:
                    row_str = " | ".join(f"{str(val)[:15]:<15}" for val in row)
                    print(row_str)
                    
                total_count = self.db.select_count_from_sqlite_table(table_name, "1=1")
                if total_count > 5:
                    print(f"\n... and {total_count - 5} more items")
            else:
                print("\n💡 This storage space is empty - no items stored yet.")
                
        except Exception as e:
            print(f"Couldn't load the data: {e}")

    def _explorer_add_storage(self):
        """Create new table in user-friendly terms"""
        print("\n➕ CREATING NEW STORAGE SPACE")
        print("="*40)
        print("Let's create a new place to store your information!")
        print("Think of this like creating a new filing cabinet or spreadsheet.")
        
        # Get storage name
        storage_name = input("\nWhat would you like to call this storage space? ").strip()
        if not storage_name:
            print("Please give your storage space a name.")
            return
            
        # Validate name
        is_valid, message = self.db.validate_table_name(storage_name)
        if not is_valid:
            print(f"⚠️  That name won't work: {message}")
            print("Try a simple name with letters, numbers, and underscores only.")
            return
            
        print(f"\nGreat! Creating storage space called '{storage_name}'")
        print("\nNow let's define what information you want to store:")
        print("(Think of each field like a column in a spreadsheet)")
        
        columns = []
        field_num = 1
        
        # Auto-add ID field
        print(f"\n📋 Field {field_num}: ID (automatic)")
        print("   This will automatically number your items (1, 2, 3...)")
        columns.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
        field_num += 1
        
        while True:
            print(f"\n📋 Field {field_num}:")
            field_name = input("  What information do you want to store? (or 'done' to finish): ").strip()
            
            if field_name.lower() == 'done':
                break
                
            if not field_name:
                print("  Please enter a name for this field.")
                continue
                
            # Simplify data type selection
            print("\n  What type of information is this?")
            print("  1. Text/Words (names, descriptions, etc.)")
            print("  2. Numbers (age, quantity, price, etc.)")
            print("  3. Yes/No (true/false)")
            print("  4. Date/Time")
            
            try:
                type_choice = int(input("  Choose type (1-4): ").strip())
                
                if type_choice == 1:
                    data_type = "TEXT"
                elif type_choice == 2:
                    data_type = "REAL"  # Use REAL for numbers to handle decimals
                elif type_choice == 3:
                    data_type = "INTEGER"
                    print("  (Will store as 1 for Yes, 0 for No)")
                elif type_choice == 4:
                    data_type = "TEXT"
                    print("  (Will store dates as text like '2025-05-30')")
                else:
                    print("  Using text type as default.")
                    data_type = "TEXT"
                    
            except ValueError:
                print("  Using text type as default.")
                data_type = "TEXT"
            
            # Ask about requirements
            required = input("  Is this information required? (y/n): ").strip().lower() == 'y'
            
            # Build field definition
            field_def = f"{field_name} {data_type}"
            if required:
                field_def += " NOT NULL"
                
            columns.append(field_def)
            print(f"  ✓ Added: {field_name} ({data_type}{'- Required' if required else ''})")
            field_num += 1
            
            if field_num > 10:  # Reasonable limit
                print("\n  You've added quite a few fields! Consider finishing here.")
        
        if len(columns) <= 1:  # Only ID field
            print("\nYou need at least one field besides the ID to store information.")
            return
            
        # Create the table
        try:
            columns_sql = ", ".join(columns)
            self.db.create_table_safe(storage_name, columns_sql)
            print(f"\n🎉 Success! Created storage space '{storage_name}'")
            print("You can now add information to it!")
        except Exception as e:
            print(f"\n❌ Couldn't create the storage space: {e}")

    def _explorer_update_data(self):
        """Update data in user-friendly terms"""
        print("\n✏️  UPDATING INFORMATION")
        print("="*40)
        print("💡 This feature will be enhanced in future versions!")
        print("For now, you can use 'Insert Data' from the main menu.")

    def _explorer_search_data(self):
        """Search data in user-friendly terms"""
        print("\n🔍 SEARCHING YOUR DATA")
        print("="*40)
        
        tables = self.db.get_tables()
        if not tables:
            print("💡 You don't have any data to search yet!")
            return
            
        print("Which storage space would you like to search?")
        for i, table in enumerate(tables, 1):
            try:
                count = self.db.select_count_from_sqlite_table(table, "1=1")
                print(f"{i}. 📁 {table} ({count} items)")
            except:
                print(f"{i}. 📁 {table}")
                
        try:
            choice = int(input("\nChoose storage space (number): ").strip()) - 1
            if 0 <= choice < len(tables):
                selected_table = tables[choice]
                self._explorer_search_in_table(selected_table)
            else:
                print("Please choose a valid number.")
        except ValueError:
            print("Please enter a number.")

    def _explorer_search_in_table(self, table_name):
        """Search within a specific table"""
        print(f"\n🔍 SEARCHING IN: {table_name}")
        print("="*40)
        
        # Get columns
        columns = self.db.get_column_info(table_name)
        if not columns:
            print("Can't search this storage space right now.")
            return
            
        print("What field do you want to search in?")
        searchable_cols = []
        for i, col in enumerate(columns):
            cid, name, data_type, not_null, default_val, is_pk = col
            if data_type in ['TEXT', 'INTEGER', 'REAL']:  # Skip BLOB
                searchable_cols.append((name, data_type))
                type_desc = {'TEXT': 'Text', 'INTEGER': 'Number', 'REAL': 'Number'}.get(data_type, data_type)
                print(f"{len(searchable_cols)}. {name} ({type_desc})")
        
        if not searchable_cols:
            print("No searchable fields found.")
            return
            
        try:
            col_choice = int(input("\nChoose field to search (number): ").strip()) - 1
            if 0 <= col_choice < len(searchable_cols):
                col_name, col_type = searchable_cols[col_choice]
                search_value = input(f"What value are you looking for in '{col_name}'? ").strip()
                
                if search_value:
                    try:
                        if col_type == 'TEXT':
                            # Text search with LIKE
                            results = self.db.execute_query(
                                f"SELECT * FROM {table_name} WHERE {col_name} LIKE '%{search_value}%'"
                            )
                        else:
                            # Exact match for numbers
                            results = self.db.execute_query(
                                f"SELECT * FROM {table_name} WHERE {col_name} = '{search_value}'"
                            )
                        
                        if results:
                            print(f"\n🎯 Found {len(results)} matching items:")
                            print("-" * 50)
                            
                            # Show column headers
                            col_names = [col[1] for col in columns]
                            header = " | ".join(f"{name[:15]:<15}" for name in col_names)
                            print(header)
                            print("-" * len(header))
                            
                            # Show results
                            for row in results[:10]:  # Limit to 10 results
                                row_str = " | ".join(f"{str(val)[:15]:<15}" for val in row)
                                print(row_str)
                                
                            if len(results) > 10:
                                print(f"\n... and {len(results) - 10} more matches")
                        else:
                            print(f"\n😔 No items found with '{search_value}' in '{col_name}'")
                            
                    except Exception as e:
                        print(f"Search failed: {e}")
                        
        except ValueError:
            print("Please enter a valid number.")

    def _explorer_data_summary(self):
        """Show data summary in user-friendly terms"""
        print("\n📈 DATA SUMMARY")
        print("="*40)
        
        tables = self.db.get_tables()
        if not tables:
            print("💡 You don't have any data stored yet!")
            return
            
        print("Here's what you have stored:")
        print()
        
        total_items = 0
        for table in tables:
            try:
                count = self.db.select_count_from_sqlite_table(table, "1=1")
                total_items += count
                
                print(f"📁 {table}:")
                print(f"   Items stored: {count}")
                
                # Get column count
                columns = self.db.get_column_info(table)
                print(f"   Information fields: {len(columns)}")
                
                # Show field names
                if columns:
                    field_names = [col[1] for col in columns]
                    print(f"   Fields: {', '.join(field_names)}")
                print()
                
            except Exception as e:
                print(f"📁 {table}: Could not analyze ({e})")
                print()
        
        print(f"📊 TOTALS:")
        print(f"   Storage spaces: {len(tables)}")
        print(f"   Total items: {total_items}")

    def _explorer_help(self):
        """Show help for the explorer"""
        print("\n❓ UI EXPLORER HELP")
        print("="*40)
        print("This explorer helps you work with data without knowing database terms!")
        print()
        print("🗃️  WHAT IS A 'STORAGE SPACE'?")
        print("   Think of it like a filing cabinet, spreadsheet, or folder.")
        print("   Each storage space holds one type of information.")
        print("   Examples: 'customers', 'products', 'orders'")
        print()
        print("📋 WHAT ARE 'FIELDS'?")
        print("   These are the types of information you store.")
        print("   Like columns in a spreadsheet.")
        print("   Examples: 'name', 'age', 'email', 'price'")
        print()
        print("🎯 WHAT CAN YOU DO HERE?")
        print("   • Browse Data: See what's stored")
        print("   • Add Storage: Create new places to store information")
        print("   • Search: Find specific items")
        print("   • Summary: Get an overview of all your data")
        print()
        print("💡 TIPS:")
        print("   • Start by creating a storage space for your information")
        print("   • Give things simple, clear names")
        print("   • You can always add more fields later")
        print("   • The ID field is automatic - you don't need to worry about it")

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
                self.ui_explorer()
            elif choice == 11:
                self.close_database()
            elif choice == 12:
                self.close_database()
                print("Thank you for using SQLite Database Manager!")
                sys.exit(0)
            elif choice is not None:
                print("Invalid choice. Please select a number between 1 and 12.")

            input("\nPress Enter to continue...")


if __name__ == "__main__":
    ui = DatabaseTerminalUI()
    ui.run()

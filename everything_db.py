import sqlite3
import os
from datetime import datetime


class SQLiteDatabase:
    def __init__(self, db_name):
        # Ensure data directory exists
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Set up database path in data directory
        if not db_name.endswith(".db"):
            db_name += ".db"
        self.db_name = os.path.join(self.data_dir, db_name)

    def create_sqlite_db(self, metadata=None):
        """Create database and store metadata"""
        is_new_db = not os.path.exists(self.db_name)

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create metadata table if it doesn't exist
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS _database_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """
        )

        conn.commit()
        conn.close()

        # If it's a new database and metadata is provided, save it
        if is_new_db and metadata:
            self.save_metadata(metadata)

        return True

    def create_sqlite_table(self, table_name, columns):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE {table_name} ({columns})")
        conn.commit()
        conn.close()
        return True

    def insert_into_sqlite_table(self, table_name, values):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} VALUES ({values})")
        conn.commit()
        conn.close()
        return True

    def delete_from_sqlite_table(self, table_name, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        conn.commit()
        conn.close()
        return True

    def update_sqlite_table(self, table_name, set_clause, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}")
        conn.commit()
        conn.close()
        return True

    def select_from_sqlite_table(self, table_name, columns, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def select_all_from_sqlite_table(self, table_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def select_distinct_from_sqlite_table(self, table_name, columns, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {columns} FROM {table_name} WHERE {condition}")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def select_count_from_sqlite_table(self, table_name, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {condition}")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def select_sum_from_sqlite_table(self, table_name, column, condition):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT SUM({column}) FROM {table_name} WHERE {condition}")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def get_tables(self):
        """Get list of all tables in the database (excluding metadata table)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != '_database_metadata'"
        )
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    def execute_query(self, query):
        """Execute a raw SQL query and return results"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            conn.commit()
            conn.close()
            return None

    def get_table_schema(self, table_name):
        """Get schema information for a table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            # Check if table exists first
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,),
            )
            if not cursor.fetchone():
                conn.close()
                return None

            cursor.execute(f"PRAGMA table_info({table_name})")
            schema = cursor.fetchall()
            conn.close()
            return schema
        except sqlite3.OperationalError:
            conn.close()
            return None

    def insert_data(self, table_name, data):
        """Insert data into a table using a dictionary"""
        if not data:
            return False

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = list(data.values())

        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values
        )
        conn.commit()
        conn.close()
        return True

    def get_table_data(self, table_name, limit=10):
        """Get data from a table with optional limit"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        data = cursor.fetchall()
        conn.close()
        return data

    def close(self):
        """Close database connection (placeholder for compatibility)"""
        # SQLite connections are closed after each operation in this implementation
        pass

    def table_exists(self, table_name):
        """Check if a table exists in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    def get_column_info(self, table_name):
        """Get detailed column information for a table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            conn.close()
            return columns
        except sqlite3.OperationalError:
            conn.close()
            return []

    def validate_table_name(self, table_name):
        """Validate table name according to SQLite rules"""
        if not table_name:
            return False, "Table name cannot be empty"

        # Check for reserved keywords (basic list)
        reserved_words = {
            "select",
            "from",
            "where",
            "insert",
            "update",
            "delete",
            "create",
            "drop",
            "alter",
            "table",
            "index",
            "view",
            "database",
            "schema",
            "primary",
            "foreign",
            "key",
            "constraint",
            "unique",
            "null",
            "not",
            "and",
            "or",
        }

        if table_name.lower() in reserved_words:
            return False, f"'{table_name}' is a reserved keyword"

        # Check if starts with underscore (reserved for system tables)
        if table_name.startswith("_") and table_name != "_database_metadata":
            return (
                False,
                "Table names starting with underscore are reserved for system use",
            )

        # Check for valid characters (letters, numbers, underscore)
        import re

        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", table_name):
            return (
                False,
                "Table name must start with a letter and contain only letters, numbers, and underscores",
            )

        return True, "Valid table name"

    def create_table_safe(self, table_name, columns):
        """Create table with validation and better error handling"""
        # Validate table name
        is_valid, message = self.validate_table_name(table_name)
        if not is_valid:
            raise ValueError(f"Invalid table name: {message}")

        # Check if table already exists
        if self.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' already exists")

        # Create the table
        try:
            self.create_sqlite_table(table_name, columns)
            return True
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to create table: {str(e)}")

    def save_metadata(self, metadata):
        """Save database metadata to database table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Ensure metadata table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS _database_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """
        )

        # Add default metadata
        metadata_data = {
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "database_name": os.path.basename(self.db_name),
            **metadata,
        }

        # Insert or replace each metadata key-value pair
        for key, value in metadata_data.items():
            if isinstance(value, list):
                value = ",".join(value)  # Convert lists to comma-separated strings
            cursor.execute(
                "INSERT OR REPLACE INTO _database_metadata (key, value) VALUES (?, ?)",
                (key, str(value)),
            )

        conn.commit()
        conn.close()

    def get_metadata(self):
        """Get database metadata from database table"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT key, value FROM _database_metadata")
            rows = cursor.fetchall()

            if not rows:
                conn.close()
                return None

            metadata = {}
            for key, value in rows:
                # Convert comma-separated strings back to lists for tags
                if key == "tags" and value:
                    metadata[key] = [
                        tag.strip() for tag in value.split(",") if tag.strip()
                    ]
                else:
                    metadata[key] = value

            conn.close()
            return metadata

        except sqlite3.OperationalError:
            # Metadata table doesn't exist
            conn.close()
            return None

    def update_metadata(self, new_metadata):
        """Update existing metadata"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Ensure metadata table exists
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS _database_metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """
        )

        # Add last_modified timestamp
        new_metadata["last_modified"] = datetime.now().isoformat()

        # Update each metadata key-value pair
        for key, value in new_metadata.items():
            if isinstance(value, list):
                value = ",".join(value)  # Convert lists to comma-separated strings
            cursor.execute(
                "INSERT OR REPLACE INTO _database_metadata (key, value) VALUES (?, ?)",
                (key, str(value)),
            )

        conn.commit()
        conn.close()

    def list_all_databases(self):
        """List all databases in the data directory with their metadata"""
        databases = []
        if not os.path.exists(self.data_dir):
            return databases

        for file in os.listdir(self.data_dir):
            if file.endswith(".db"):
                db_name = os.path.splitext(file)[0]
                db_path = os.path.join(self.data_dir, file)

                db_info = {"name": db_name, "file": file, "path": db_path}

                # Get metadata from the database itself
                try:
                    temp_db = SQLiteDatabase(db_name)
                    metadata = temp_db.get_metadata()
                    db_info["metadata"] = metadata
                except Exception:
                    db_info["metadata"] = None

                databases.append(db_info)

        return databases

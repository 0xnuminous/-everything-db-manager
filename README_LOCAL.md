# SQLite Database Manager

A terminal-based SQLite database management tool with metadata support and organized file structure.

## Features

- **Database Management**: Create, open, and manage SQLite databases
- **Metadata Support**: Store and retrieve database descriptions, purpose, owner, and tags
- **Organized Storage**: All databases stored in dedicated `data/` directory
- **Table Operations**: Create, view, and manage database tables
- **Query Execution**: Execute custom SQL queries
- **Data Management**: Insert, view, and manipulate table data
- **Schema Inspection**: View table structures and column information

## File Structure

```
everything/
├── data/                    # Database storage directory
│   └── *.db                # SQLite database files (with internal metadata)
├── everything_db.py         # Database class with SQLite operations
├── everything_ui.py         # Terminal user interface
└── README.md               # This documentation
```

## Quick Start

1. Run the application:
   ```bash
   uv run everything_ui.py
   ```

2. Choose option 1 to create or open a database
3. For new databases, provide metadata:
   - Description: Brief overview of the database
   - Purpose/Project: What this database is used for
   - Owner/Creator: Who created/maintains it
   - Tags: Comma-separated keywords for organization

## Menu Options

1. **Open/Create Database** - Create new or open existing database
2. **List All Databases** - View all databases with metadata
3. **List Tables** - Show tables in current database
4. **Create Table** - Interactive or manual table creation
5. **Execute Query** - Run custom SQL commands
6. **Show Table Schema** - Display table structure
7. **Insert Data** - Add data using column=value format
8. **View Table Data** - Display table contents with optional limit
9. **Show Database Info** - View current database metadata
10. **Close Database** - Close current database connection
11. **Exit** - Quit the application

## Database Metadata

Each database automatically stores metadata internally in a special `_database_metadata` table:
- Creation date
- Last modified date
- Description
- Purpose/Project
- Owner/Creator
- Tags for categorization

The metadata table is hidden from normal table operations but accessible through the metadata methods.

## Usage Examples

### Creating a Database
1. Select "Create new database"
2. Enter name: `inventory_system`
3. Provide metadata:
   - Description: "Store and track inventory items"
   - Purpose: "E-commerce inventory management"
   - Owner: "John Doe"
   - Tags: "inventory, ecommerce, products"

### Creating a Table

#### Option 1: Interactive Table Creation
1. Select "Create Table" from menu
2. Choose "Interactive table creation (guided)"
3. Enter table name: `products`
4. Define columns step by step:
   - Column 1: `id` (INTEGER, Primary Key, Auto Increment)
   - Column 2: `name` (TEXT, Not Null)
   - Column 3: `price` (REAL, Not Null)
   - Column 4: `quantity` (INTEGER, Default: 0)

#### Option 2: Manual SQL Definition
1. Select "Create Table" from menu
2. Choose "Manual SQL definition"
3. Enter table name: `products`
4. Enter column definitions:
```
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
price REAL NOT NULL CHECK(price >= 0),
quantity INTEGER DEFAULT 0
```

#### Option 3: Execute Query
Use the "Execute Query" option with SQL:
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    quantity INTEGER DEFAULT 0
)
```

### Inserting Data
Use the "Insert Data" option with format:
```
name=Widget A
price=19.99
quantity=100
```

## SQLiteDatabase Class Methods

### Core Operations
- `create_sqlite_db(metadata=None)` - Create database with optional metadata
- `create_sqlite_table(table_name, columns)` - Create new table
- `insert_into_sqlite_table(table_name, values)` - Insert raw SQL values
- `select_from_sqlite_table(table_name, columns, condition)` - Select with condition
- `update_sqlite_table(table_name, set_clause, condition)` - Update records
- `delete_from_sqlite_table(table_name, condition)` - Delete records

### High-Level Methods
- `get_tables()` - List all tables (excludes metadata table)
- `execute_query(query)` - Execute any SQL query
- `get_table_schema(table_name)` - Get table column information
- `insert_data(table_name, data)` - Insert using dictionary
- `get_table_data(table_name, limit=10)` - Retrieve table data

### Table Management Methods
- `create_table_safe(table_name, columns)` - Create table with validation
- `table_exists(table_name)` - Check if table exists
- `get_column_info(table_name)` - Get detailed column information
- `validate_table_name(table_name)` - Validate table name rules

### Metadata Methods
- `save_metadata(metadata)` - Store database metadata in internal table
- `get_metadata()` - Retrieve database metadata from internal table
- `update_metadata(new_metadata)` - Update existing metadata in internal table
- `list_all_databases()` - List all databases with metadata from internal storage

## Requirements

- uv (Python package manager)
- Python 3.12+ (managed by uv)
- sqlite3 (included in Python standard library)
- json (included in Python standard library)
- os (included in Python standard library)
- datetime (included in Python standard library)

### Installation

1. Install uv:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Initialize the project:
   ```bash
   cd everything
   uv sync  # Sets up virtual environment and dependencies
   ```

## Data Directory

All databases are automatically stored in the `data/` directory:
- Database files: `database_name.db` (includes internal metadata table)

The data directory is created automatically if it doesn't exist. Metadata is stored within each database file in a special `_database_metadata` table, eliminating the need for separate metadata files.

## Table Creation Features

### Interactive Table Creation
- **Guided Process**: Step-by-step column definition
- **Flexible Data Types**: Accepts common abbreviations (int, string, float, etc.)
- **Constraint Support**: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT values
- **Auto Increment**: Available for INTEGER primary keys
- **Validation**: Prevents invalid table names and duplicate tables
- **Real-time Feedback**: Shows column definitions as you build them

### Manual Table Creation
- **SQL Definition**: Direct column definition entry
- **Advanced Constraints**: Support for CHECK constraints, foreign keys
- **Complex Types**: Full SQLite type and constraint syntax
- **Preview**: Shows final SQL before creation

### Table Name Validation
- **Reserved Words**: Prevents use of SQL keywords
- **System Tables**: Blocks underscore-prefixed names (except metadata)
- **Character Rules**: Enforces valid identifier syntax
- **Duplicate Check**: Prevents overwriting existing tables

### Supported Data Types
- **INTEGER**: Whole numbers, can be PRIMARY KEY with AUTOINCREMENT
  - Accepts: `INTEGER`, `INT`
- **TEXT**: String data of any length
  - Accepts: `TEXT`, `STRING`, `VARCHAR`, `CHAR`
- **REAL**: Floating-point numbers
  - Accepts: `REAL`, `FLOAT`, `DOUBLE`, `DECIMAL`
- **BLOB**: Binary data
  - Accepts: `BLOB`, `BINARY`

### Supported Constraints
- **PRIMARY KEY**: Unique identifier, automatically indexed
- **NOT NULL**: Prevents empty values
- **UNIQUE**: Ensures unique values across rows
- **DEFAULT**: Sets default value for new rows
- **CHECK**: Validates data against conditions
- **FOREIGN KEY**: References other tables (manual SQL only)

## User Interface Improvements

### Enhanced Schema Display
- **Formatted Tables**: Clean, readable column information
- **Column Details**: Shows type, nullable status, keys, and defaults
- **Error Handling**: Clear messages for non-existent tables
- **Table Suggestions**: Lists available tables when one isn't found

### Improved Data Entry
- **Input Examples**: Shows format examples for data entry
- **Duplicate Detection**: Warns when overwriting column values
- **Quote Handling**: Automatically handles quoted string values
- **Real-time Feedback**: Confirms each column=value pair as entered
- **Table Validation**: Checks table existence before allowing data entry

### Better Error Messages
- **Context-Aware**: Provides relevant suggestions based on current state
- **Helpful Guidance**: Shows available options when operations fail
- **Clear Formatting**: Well-structured error messages and warnings
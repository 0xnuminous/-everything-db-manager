# Table Creation Quick Reference Guide

## Overview

The SQLite Database Manager provides two ways to create tables:
1. **Interactive Creation** - Guided step-by-step process
2. **Manual SQL Definition** - Direct SQL input

## Access Table Creation

1. Open database (Menu option 1)
2. Select "Create Table" (Menu option 4)
3. Choose creation method

## Interactive Creation

### Step-by-Step Process

1. **Table Name**: Enter valid table name
2. **Column Definition**: For each column specify:
   - Column name
   - Data type (INTEGER, TEXT, REAL, BLOB)
   - Primary key (y/n)
   - Auto increment (for INTEGER primary keys)
   - Not null constraint (y/n)
   - Unique constraint (y/n)
   - Default value (optional)

### Example Interactive Session

```
Table name: users
Column 1: id
  Data type: INTEGER
  Primary key: y
  Auto increment: y
  Result: id INTEGER PRIMARY KEY AUTOINCREMENT

Column 2: username
  Data type: TEXT
  Primary key: n
  Not null: y
  Unique: y
  Result: username TEXT NOT NULL UNIQUE

Column 3: email
  Data type: TEXT
  Primary key: n
  Not null: y
  Unique: y
  Result: email TEXT NOT NULL UNIQUE

Column 4: created_at
  Data type: TEXT
  Primary key: n
  Not null: n
  Unique: n
  Default: CURRENT_TIMESTAMP
  Result: created_at TEXT DEFAULT CURRENT_TIMESTAMP
```

## Manual SQL Definition

### Format
```
table_name: your_table_name
Column definitions: column1 TYPE constraints, column2 TYPE constraints, ...
```

### Example Manual Definition

```
Table name: products
Column definitions:
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
description TEXT,
price REAL NOT NULL CHECK(price >= 0),
stock_quantity INTEGER DEFAULT 0,
category_id INTEGER,
created_at TEXT DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (category_id) REFERENCES categories(id)
```

## Data Types

| Type    | Description           | Example Values        |
|---------|----------------------|-----------------------|
| INTEGER | Whole numbers        | 1, -5, 1000          |
| TEXT    | String data          | 'Hello', 'User Name'  |
| REAL    | Decimal numbers      | 3.14, -2.5, 100.0    |
| BLOB    | Binary data          | Images, files         |

## Common Constraints

| Constraint           | Purpose                    | Example                    |
|---------------------|----------------------------|----------------------------|
| PRIMARY KEY         | Unique identifier          | `id INTEGER PRIMARY KEY`   |
| AUTOINCREMENT       | Auto-incrementing numbers  | `PRIMARY KEY AUTOINCREMENT`|
| NOT NULL            | Prevents empty values      | `name TEXT NOT NULL`       |
| UNIQUE              | Ensures unique values      | `email TEXT UNIQUE`        |
| DEFAULT             | Sets default value         | `status TEXT DEFAULT 'active'` |
| CHECK               | Validates data             | `age INTEGER CHECK(age >= 0)` |
| FOREIGN KEY         | References other table     | `FOREIGN KEY (user_id) REFERENCES users(id)` |

## Table Name Rules

### Valid Names
- Must start with a letter
- Can contain letters, numbers, underscores
- Examples: `users`, `user_profiles`, `table_123`

### Invalid Names
- Reserved SQL keywords: `select`, `from`, `where`, `table`
- System tables: `_private`, `_system` (underscore prefix)
- Starting with numbers: `123table`
- Special characters: `user-table`, `user.table`

## Common Table Patterns

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    full_name TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1
)
```

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL CHECK(price >= 0),
    stock_quantity INTEGER DEFAULT 0,
    category_id INTEGER,
    sku TEXT UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL CHECK(total_amount > 0),
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    order_date TEXT DEFAULT CURRENT_TIMESTAMP,
    shipping_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
```

### Junction/Many-to-Many Table
```sql
CREATE TABLE user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_at TEXT DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
)
```

## Tips

1. **Start Simple**: Begin with basic tables, add constraints later
2. **Use AUTO INCREMENT**: For primary keys that should auto-generate
3. **Add Timestamps**: Include `created_at` and `updated_at` fields
4. **Validate Data**: Use CHECK constraints for data validation
5. **Plan Relationships**: Consider foreign keys for related data
6. **Consistent Naming**: Use consistent naming conventions (snake_case)

## Error Prevention

- Preview your table definition before creating
- Check for typos in column names and types
- Verify constraint syntax
- Ensure foreign key references exist
- Avoid reserved keywords for table/column names

## After Creation

1. **Verify Structure**: Use "Show Table Schema" (Menu option 6)
2. **Insert Test Data**: Use "Insert Data" (Menu option 7)
3. **Query Data**: Use "Execute Query" (Menu option 5)
4. **View Contents**: Use "View Table Data" (Menu option 8)
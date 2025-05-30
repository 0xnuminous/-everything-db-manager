# Development Guide

## Prerequisites

This project uses **uv** as the Python package manager. Install it first:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Project Setup

### Initialize Development Environment

```bash
# Clone or navigate to project
cd everything

# Initialize virtual environment and install dependencies
uv sync

# Verify setup
uv run python -c "from everything_db import SQLiteDatabase; print('✓ Setup complete')"
```

## Running the Application

### Start the Main Application
```bash
# Interactive database manager
uv run everything_ui.py

# Or use the run script
uv run run.py
```

### Run Demo Scripts
```bash
# Basic usage examples
uv run example_usage.py

# Table creation demonstration
uv run table_creation_demo.py

# UI improvements showcase
uv run ui_improvements_demo.py

# UI Explorer beginner-friendly interface
uv run ui_explorer_demo.py
```

## Development Commands

### Code Testing
```bash
# Test database functionality
uv run python -c "from everything_db import SQLiteDatabase; db = SQLiteDatabase('test'); print('✓ Database works')"

# Test UI components
uv run python -c "from everything_ui import DatabaseTerminalUI; ui = DatabaseTerminalUI(); print('✓ UI works')"

# Verify all imports
uv run python -c "
import everything_db
import everything_ui
print('✓ All modules import successfully')
"
```

### Check Python Version
```bash
# Show current Python version used by uv
uv python list

# Install specific Python version if needed
uv python install 3.12
```

### Virtual Environment Management
```bash
# Show virtual environment info
uv venv --help

# Recreate virtual environment if needed
rm -rf .venv
uv sync
```

## Project Structure

```
everything/
├── data/                    # Database storage directory
│   ├── .gitkeep            # Keeps directory in git
│   └── *.db                # SQLite database files
├── everything_db.py         # Database operations class
├── everything_ui.py         # Terminal user interface
├── run.py                   # Application entry point
├── example_usage.py         # Usage demonstration
├── table_creation_demo.py   # Table creation examples
├── ui_improvements_demo.py  # UI enhancements demo
├── ui_explorer_demo.py      # UI Explorer demonstration
├── pyproject.toml          # Project configuration
├── README.md               # User documentation
├── DEVELOPMENT.md          # This file
└── *.md                    # Additional documentation
```

## Database Management

### Clean Test Data
```bash
# Remove test databases
rm -f data/test*.db data/example*.db data/*demo*.db

# Keep only production databases
ls data/
```

### Backup Databases
```bash
# Create backup of important databases
cp data/important.db data/important.db.backup

# Or backup entire data directory
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/
```

## Adding Dependencies

```bash
# Add runtime dependency
uv add requests

# Add development dependency
uv add --dev pytest

# Add with version constraint
uv add "ruff>=0.2.0"

# Install from git
uv add "git+https://github.com/user/repo"
```

## Code Quality

### Formatting (if ruff is added)
```bash
# Format code
uv run ruff format .

# Check code
uv run ruff check .
```

### Testing (if pytest is added)
```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov
```

## Features Overview

### Core Features
- **Database Management**: Create, open, and manage SQLite databases
- **Table Operations**: Interactive and manual table creation with validation
- **Data Management**: Insert, query, update, and delete operations
- **Schema Inspection**: View table structures and relationships
- **Metadata System**: Internal storage of database descriptions and tags

### UI Explorer (Beginner-Friendly)
- **Plain Language Interface**: Uses everyday terms instead of technical jargon
- **Guided Workflows**: Step-by-step processes for common tasks
- **Visual Data Display**: Clean, formatted views of stored information
- **Smart Search**: Find data without SQL knowledge
- **Data Summaries**: Overview of all stored information
- **Interactive Help**: Built-in explanations and guidance

## Environment Variables

### UV Configuration
```bash
# Specify Python version
export UV_PYTHON=3.12

# Custom tool installation directory
export UV_TOOL_DIR=/custom/path

# Disable cache
export UV_NO_CACHE=1
```

### Application Configuration
```bash
# Custom data directory (if implemented)
export EVERYTHING_DATA_DIR=/custom/data

# Debug mode (if implemented)
export EVERYTHING_DEBUG=1
```

## Troubleshooting

### Common Issues

**Virtual Environment Conflicts:**
```bash
# Clear existing environment
rm -rf .venv
uv sync
```

**Import Errors:**
```bash
# Verify current directory
pwd
# Should be in /path/to/everything

# Check Python path
uv run python -c "import sys; print(sys.path)"
```

**Database Permission Errors:**
```bash
# Check data directory permissions
ls -la data/
chmod 755 data/
```

### Debug Commands
```bash
# Show uv environment info
uv info

# Show project configuration
cat pyproject.toml

# List installed packages
uv pip list

# Show virtual environment location
uv venv --help
```

## Performance Tips

### Database Optimization
- Use transactions for bulk operations
- Add indexes for frequently queried columns
- Regular `VACUUM` operations for large databases

### Application Performance
```bash
# Profile application startup
uv run python -m cProfile everything_ui.py

# Memory usage monitoring (if psutil is added)
uv add psutil
uv run python -c "import psutil; print(f'Memory: {psutil.virtual_memory()}')"
```

## Contributing Workflow

1. **Setup Development Environment:**
   ```bash
   uv sync
   ```

2. **Make Changes:**
   ```bash
   # Edit files
   # Test changes
   uv run example_usage.py
   ```

3. **Test Changes:**
   ```bash
   # Run all demo scripts
   uv run example_usage.py
   uv run table_creation_demo.py
   uv run ui_improvements_demo.py
   ```

4. **Document Changes:**
   ```bash
   # Update README.md if needed
   # Update this DEVELOPMENT.md if needed
   ```

## Release Process

### Version Updates
```bash
# Update version in pyproject.toml
# Test all functionality
uv run example_usage.py

# Clean test data
rm -f data/test*.db data/example*.db

# Verify clean state
ls data/
```

### Documentation Updates
- Update README.md with new features
- Update TABLE_CREATION_GUIDE.md if table features changed
- Update IMPROVEMENTS_SUMMARY.md with new improvements

## Useful uv Commands Reference

```bash
# Project management
uv init project-name          # Initialize new project
uv add package-name           # Add dependency
uv remove package-name        # Remove dependency
uv sync                       # Install dependencies
uv lock                       # Generate lock file

# Python management
uv python install 3.12       # Install Python version
uv python list                # List available versions
uv python pin 3.12            # Pin project to version

# Tool management
uv tool install ruff          # Install global tool
uv tool list                  # List installed tools
uvx tool-name                 # Run tool temporarily

# Environment management
uv venv                       # Create virtual environment
uv run command                # Run in project environment
uv pip install package       # Install with pip interface

# Information
uv info                       # Show environment info
uv --version                  # Show uv version
uv self update                # Update uv itself
```
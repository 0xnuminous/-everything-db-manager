#!/usr/bin/env python3
"""
Verification script to test uv setup and all components
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        import everything_db
        print("✓ everything_db imported successfully")
        
        import everything_ui
        print("✓ everything_ui imported successfully")
        
        from everything_db import SQLiteDatabase
        print("✓ SQLiteDatabase class imported successfully")
        
        from everything_ui import DatabaseTerminalUI
        print("✓ DatabaseTerminalUI class imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_database_creation():
    """Test database creation and basic operations"""
    print("\nTesting database operations...")
    try:
        from everything_db import SQLiteDatabase
        # Create test database
        db = SQLiteDatabase("verify_test")
        db.create_sqlite_db({
            "description": "Verification test database",
            "owner": "Setup Verification",
            "purpose": "Testing uv setup"
        })
        print("✓ Database creation successful")
        
        # Test metadata
        metadata = db.get_metadata()
        if metadata and metadata.get("description") == "Verification test database":
            print("✓ Metadata storage and retrieval successful")
        else:
            print("✗ Metadata test failed")
            return False
        
        # Test table creation
        db.create_table_safe("test_table", "id INTEGER PRIMARY KEY, name TEXT")
        if db.table_exists("test_table"):
            print("✓ Table creation successful")
        else:
            print("✗ Table creation failed")
            return False
        
        # Test data insertion
        db.insert_data("test_table", {"name": "test_record"})
        data = db.get_table_data("test_table", 1)
        if data and len(data) > 0:
            print("✓ Data insertion and retrieval successful")
        else:
            print("✗ Data operations failed")
            return False
        
        # Cleanup
        os.remove("data/verify_test.db")
        print("✓ Test database cleaned up")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_ui_initialization():
    """Test UI initialization"""
    print("\nTesting UI initialization...")
    try:
        from everything_ui import DatabaseTerminalUI
        ui = DatabaseTerminalUI()
        if hasattr(ui, 'display_menu') and hasattr(ui, 'get_user_choice'):
            print("✓ UI initialization successful")
            return True
        else:
            print("✗ UI missing required methods")
            return False
    except Exception as e:
        print(f"✗ UI initialization failed: {e}")
        return False

def test_data_directory():
    """Test data directory structure"""
    print("\nTesting data directory...")
    data_dir = Path("data")
    if data_dir.exists() and data_dir.is_dir():
        print("✓ Data directory exists")
        
        gitkeep = data_dir / ".gitkeep"
        if gitkeep.exists():
            print("✓ .gitkeep file present")
        else:
            print("! .gitkeep file missing (not critical)")
        
        return True
    else:
        print("✗ Data directory missing")
        return False

def test_python_version():
    """Test Python version compatibility"""
    print("\nTesting Python version...")
    version = sys.version_info
    if version >= (3, 12):
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"! Python {version.major}.{version.minor}.{version.micro} (may have compatibility issues)")
        return True  # Don't fail for version issues

def test_standard_library():
    """Test required standard library modules"""
    print("\nTesting standard library modules...")
    try:
        import sqlite3
        print("✓ sqlite3 available")
        
        import json
        print("✓ json available")
        
        import os
        print("✓ os available")
        
        import datetime
        print("✓ datetime available")
        
        return True
    except ImportError as e:
        print(f"✗ Standard library test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("SQLite Database Manager - Setup Verification")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_standard_library,
        test_data_directory,
        test_imports,
        test_database_creation,
        test_ui_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Verification Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Setup is working correctly.")
        print("\nNext steps:")
        print("  - Run 'uv run everything_ui.py' to start the application")
        print("  - Run 'uv run example_usage.py' to see examples")
        print("  - Run 'uv run table_creation_demo.py' for table creation demo")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
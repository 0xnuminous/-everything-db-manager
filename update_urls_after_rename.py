#!/usr/bin/env python3
"""
Script to update all repository URLs after renaming from -everything-db-manager to everything-db-manager
Run this script after renaming the repository on GitHub.
"""

import os
import re
from pathlib import Path

def update_file_urls(file_path, old_url, new_url):
    """Update URLs in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = content.replace(old_url, new_url)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {file_path}")
            return True
        else:
            print(f"  No changes: {file_path}")
            return False
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")
        return False

def main():
    """Update all repository URLs in documentation files"""
    print("Repository URL Update Script")
    print("=" * 40)
    
    # Define URL patterns to replace
    old_url = "0xnuminous/-everything-db-manager"
    new_url = "0xnuminous/everything-db-manager"
    
    # Files to update
    files_to_update = [
        "README.md",
        "GITHUB_SETUP.md", 
        "DEPLOYMENT_SUCCESS.md",
        "AI_DEVELOPMENT_PROCESS.md",
        "CONTRIBUTING.md",
        "DEVELOPMENT.md",
        "UV_MIGRATION_SUMMARY.md"
    ]
    
    updated_count = 0
    
    print(f"Updating URLs from: {old_url}")
    print(f"                to: {new_url}")
    print()
    
    for file_name in files_to_update:
        file_path = Path(file_name)
        if file_path.exists():
            if update_file_urls(file_path, old_url, new_url):
                updated_count += 1
        else:
            print(f"  File not found: {file_name}")
    
    print()
    print(f"Summary: Updated {updated_count} files")
    
    if updated_count > 0:
        print()
        print("Next steps:")
        print("1. Review the changes with: git diff")
        print("2. Commit the changes:")
        print("   git add .")
        print('   git commit -m "docs: update repository URLs after rename"')
        print("   git push")
    else:
        print("No files needed updating.")

if __name__ == "__main__":
    main()
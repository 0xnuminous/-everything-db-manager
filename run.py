#!/usr/bin/env python3
"""
Run script for SQLite Database Manager
Makes it easy to start the application with uv
"""

import sys
import os

# Add current directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from everything_ui import DatabaseTerminalUI

if __name__ == "__main__":
    ui = DatabaseTerminalUI()
    ui.run()
# Everything DB Manager

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-green.svg)](https://github.com/astral-sh/uv)
[![SQLite](https://img.shields.io/badge/database-SQLite-lightblue.svg)](https://sqlite.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AI](https://img.shields.io/badge/created%20with-Claude%20Sonnet-orange.svg)](https://claude.ai)
[![IDE](https://img.shields.io/badge/built%20in-Zed%20Agentic-purple.svg)](https://zed.dev)

A modern, fast SQLite database manager with an interactive terminal UI. Built with **uv** for lightning-fast dependency management and featuring comprehensive table creation, metadata storage, and database operations.

> 🤖 **AI-Powered Development**: This project was created collaboratively with Claude Sonnet 3.5 using Zed's innovative agentic mode, showcasing the future of AI-assisted software development.

## ✨ Features

- 🚀 **Lightning Fast**: Built with uv package manager (10-100x faster than pip)
- 📊 **Interactive Database Management**: Terminal-based UI with guided workflows
- 🛠️ **Smart Table Creation**: Both interactive guided mode and manual SQL definition
- 🏷️ **Metadata Management**: Store database descriptions, purpose, owner, and tags internally
- 🔍 **Schema Inspection**: Beautiful formatted table schemas and column information
- **Enhanced Data Entry**: Real-time feedback, validation, and error handling
- **UI Explorer**: Intuitive interface for users unfamiliar with database concepts
- **Multi-Database Support**: Manage multiple databases with organized storage
- **Modern Python Tooling**: Uses uv, Python 3.12+, and modern best practices

## 🎯 Quick Start

### Prerequisites

Install [uv](https://github.com/astral-sh/uv) - the fast Python package manager:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation

```bash
# Clone the repository
git clone https://github.com/0xnuminous/everything-db-manager.git
cd everything-db-manager

# Set up the environment (creates .venv automatically)
uv sync

# Verify installation
uv run verify_setup.py
```

### Launch the Application

```bash
# Start the interactive database manager
uv run everything_ui.py

# Or use the dedicated run script
uv run run.py
```

## 🎮 Demo & Examples

```bash
# Run the basic usage demo
uv run example_usage.py

# See table creation examples
uv run table_creation_demo.py

# View UI improvements showcase
uv run ui_improvements_demo.py
```

## 📋 Menu Options

1. **Open/Create Database** - Create new or open existing database with metadata
2. **List All Databases** - View all databases with descriptions and info
3. **List Tables** - Show tables in current database
4. **Create Table** - Interactive or manual table creation with validation
5. **Execute Query** - Run custom SQL commands
6. **Show Table Schema** - Display formatted table structure
7. **Insert Data** - Add data with guided input and validation
8. **View Table Data** - Browse table contents with pagination
9. **Show Database Info** - View database metadata and statistics
10. **UI Explorer** - Beginner-friendly interface for non-technical users
11. **Close Database** - Close current database connection
12. **Exit** - Quit the application

## 🛠️ Table Creation Features

### Interactive Mode
- **Guided Process**: Step-by-step column definition
- **Flexible Data Types**: Accepts common abbreviations (`int`, `string`, `float`, etc.)
- **Smart Constraints**: PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT values
- **Auto Increment**: Available for INTEGER primary keys
- **Real-time Preview**: Shows table definition as you build

### Manual Mode
- **SQL Definition**: Direct column definition entry
- **Advanced Features**: CHECK constraints, foreign keys, complex types
- **Syntax Validation**: Prevents common errors before creation

## 🎮 UI Explorer - Beginner-Friendly Interface

The UI Explorer provides an intuitive interface for users who aren't familiar with database terminology:

### Features
- **Plain Language**: Uses terms like "storage space" instead of "table"
- **Guided Workflows**: Step-by-step processes for common tasks
- **Visual Data Display**: Clean, formatted views of your information
- **Smart Search**: Find data without writing SQL queries
- **Data Summaries**: Overview of all stored information

### Explorer Options
1. **📊 Browse My Data** - See what information is stored
2. **➕ Add New Information** - Create new storage spaces with guided setup
3. **✏️ Update Existing Information** - Modify stored data
4. **🔍 Search & Filter Data** - Find specific items easily
5. **📈 Get Data Summary** - Overview of all your data
6. **❓ Help** - Explanations of concepts and features

### Example Workflow
```
Creating a "customers" storage space:
1. Choose a name: "customers"
2. Add fields step-by-step:
   - Name (Text/Words - Required)
   - Email (Text/Words - Required) 
   - Age (Numbers - Optional)
   - Active (Yes/No - Optional)
3. Automatically creates proper database structure
```

### Example Interactive Session
```
Table name: users
Column 1: id (INTEGER, Primary Key, Auto Increment)
Column 2: username (TEXT, Not Null, Unique)
Column 3: email (TEXT, Not Null, Unique)
Column 4: created_at (TEXT, Default: CURRENT_TIMESTAMP)
```

## 💾 Database Management

### Metadata Storage
Each database automatically stores:
- 📅 Creation and modification dates
- 📝 Description and purpose
- 👤 Owner/creator information
- 🏷️ Tags for organization

### Data Organization
```
data/
├── .gitkeep              # Maintains directory structure
├── my_project.db         # Your database files
└── inventory_system.db   # With embedded metadata
```

## 🚦 Requirements

- **Python**: 3.12+ (managed by uv)
- **Package Manager**: uv
- **Database**: SQLite 3 (included with Python)
- **OS**: Windows, macOS, Linux

## 📚 Documentation

- **[Development Guide](DEVELOPMENT.md)** - Setup and development workflow
- **[Table Creation Guide](TABLE_CREATION_GUIDE.md)** - Comprehensive table creation reference
- **[UI Improvements](IMPROVEMENTS_SUMMARY.md)** - User experience enhancements
- **[UV Migration](UV_MIGRATION_SUMMARY.md)** - Modern tooling adoption

## 🔧 Development

### Common Commands
```bash
# Setup development environment
uv sync

# Run application
uv run everything_ui.py

# Add new dependencies
uv add package-name

# Add development dependencies
uv add --dev pytest

# Run verification tests
uv run verify_setup.py
```

### Project Structure
```
everything-db-manager/
├── data/                    # Database storage
├── everything_db.py         # Core database operations
├── everything_ui.py         # Terminal interface
├── run.py                   # Application entry point
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
└── docs/                   # Documentation files
```

## 🤖 AI-Powered Development Methodology

This project demonstrates the cutting-edge capabilities of AI-assisted software development using:

### Development Process
- **Collaborative Design**: Human creativity combined with AI technical expertise
- **Iterative Enhancement**: Real-time feedback and improvement cycles
- **Modern Tooling Integration**: Seamless adoption of uv, Python 3.12+, and best practices
- **Documentation-First**: Comprehensive guides generated alongside code development
- **Quality Assurance**: Built-in validation, testing, and verification systems

### AI Capabilities Showcased
- **Full-Stack Development**: From database design to user interface implementation
- **Code Architecture**: Professional project structure and modular design patterns
- **User Experience Design**: Intuitive workflows and error handling improvements
- **Technical Writing**: Complete documentation suite including guides and examples
- **DevOps Integration**: Modern packaging, dependency management, and deployment

### Zed Agentic Mode Features
- **Real-time Collaboration**: Seamless human-AI code editing and review
- **Context Awareness**: Understanding of entire project scope and dependencies
- **Tool Integration**: Direct access to development tools and environments
- **Quality Control**: Automated testing and verification during development

> This project serves as a proof-of-concept for the future of software development, where AI assistants can collaborate as full development partners while maintaining human creativity and oversight.

## 🎨 User Interface Highlights

### Before & After Improvements

**Schema Display - Before:**
```
(0, 'id', 'INTEGER', 0, None, 1)
(1, 'name', 'TEXT', 1, None, 0)
```

**Schema Display - After:**
```
Column               Type            Nullable   Key        Default
------------------------------------------------------------
id                   INTEGER         YES        PRIMARY
name                 TEXT            NO
```

### Enhanced Features
- ✅ **Flexible Data Types**: `int` → INTEGER, `string` → TEXT
- ✅ **Beautiful Formatting**: Clean, readable table displays
- ✅ **Smart Validation**: Table existence checks with suggestions
- ✅ **Real-time Feedback**: Immediate confirmation of actions
- ✅ **Error Recovery**: Helpful messages with next steps

## 🚀 Performance

Built with **uv** for exceptional performance:
- **10-100x faster** dependency resolution vs pip
- **Instant environment creation** and management
- **Parallel package installation** by default
- **Efficient caching** for repeated operations

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Setup development environment**: `uv sync`
4. **Make your changes and test**: `uv run verify_setup.py`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### AI-Powered Development
- **[Claude Sonnet 3.5](https://claude.ai)** - AI assistant that collaboratively designed and built this entire project
- **[Zed Editor](https://zed.dev)** - Revolutionary agentic mode enabling seamless AI-human collaboration
- **Modern AI Development** - Showcasing the future of software creation through AI partnership

### Technologies & Tools
- **[uv](https://github.com/astral-sh/uv)** - Amazing Python package manager by Astral
- **SQLite** - Reliable, lightweight database engine
- **Python Community** - For excellent tooling and libraries

---

**Made with ❤️ and powered by uv**
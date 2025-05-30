# Contributing to Everything DB Manager

Thank you for your interest in contributing to the Everything DB Manager! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- **uv** - Fast Python package manager
- **Python 3.12+** (managed by uv)
- **Git** for version control

### Installation

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/everything-db-manager.git
cd everything-db-manager

# Set up development environment
uv sync

# Verify setup
uv run verify_setup.py
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 3. Test Your Changes

```bash
# Run verification tests
uv run verify_setup.py

# Test all demo scripts
uv run example_usage.py
uv run table_creation_demo.py
uv run ui_improvements_demo.py

# Test the main application
uv run everything_ui.py
```

### 4. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "feat: add new table validation feature

- Add foreign key constraint validation
- Improve error messages for invalid constraints
- Update tests and documentation"
```

#### Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference any related issues
- List changes made
- Include screenshots if UI changes

## Code Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example Code Style

```python
def create_table_safe(self, table_name: str, columns: str) -> bool:
    """Create table with validation and better error handling.
    
    Args:
        table_name: Name of the table to create
        columns: SQL column definitions
        
    Returns:
        True if table created successfully
        
    Raises:
        ValueError: If table name is invalid or table exists
        sqlite3.Error: If SQL execution fails
    """
    # Validate table name
    is_valid, message = self.validate_table_name(table_name)
    if not is_valid:
        raise ValueError(f"Invalid table name: {message}")
    
    # Implementation...
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Update README.md for new features
- Add inline comments for complex logic

## Testing Guidelines

### Manual Testing

Before submitting a PR, test:

1. **Core Functionality**
   ```bash
   uv run verify_setup.py
   ```

2. **Database Operations**
   - Create/open databases
   - Table creation (both modes)
   - Data insertion and retrieval
   - Schema inspection

3. **User Interface**
   - Menu navigation
   - Error handling
   - Input validation
   - Help messages

4. **Edge Cases**
   - Invalid table names
   - Duplicate operations
   - Large datasets
   - Special characters

### Demo Scripts

Ensure all demo scripts work:
```bash
uv run example_usage.py
uv run table_creation_demo.py
uv run ui_improvements_demo.py
```

## Adding New Features

### Database Features

When adding database functionality:

1. **Add to `everything_db.py`**
   - Follow existing method patterns
   - Include proper error handling
   - Add validation where needed

2. **Update UI in `everything_ui.py`**
   - Add menu option if needed
   - Provide user feedback
   - Handle errors gracefully

3. **Create Demo**
   - Add example to demo scripts
   - Show feature in action

### UI Improvements

For UI enhancements:

1. **Maintain Consistency**
   - Follow existing formatting patterns
   - Use consistent terminology
   - Provide clear feedback

2. **Error Handling**
   - Clear error messages
   - Suggest next actions
   - Graceful degradation

3. **User Experience**
   - Intuitive workflows
   - Helpful prompts
   - Progress indicators

## Adding Dependencies

### Runtime Dependencies

```bash
# Add new runtime dependency
uv add package-name

# Add with version constraint
uv add "package-name>=1.0.0"
```

### Development Dependencies

```bash
# Add development dependency
uv add --dev package-name
```

### Update Lock File

```bash
# Update dependencies
uv sync
```

## Documentation Updates

When adding features:

1. **Update README.md** with new functionality
2. **Add to DEVELOPMENT.md** if developer-facing
3. **Update guides** in `TABLE_CREATION_GUIDE.md` etc.
4. **Add examples** to demo scripts

## Issue Reporting

### Bug Reports

Include:
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment** (OS, Python version, uv version)
- **Error messages** (full traceback)

### Feature Requests

Include:
- **Use case** description
- **Proposed solution**
- **Alternative solutions** considered
- **Additional context**

## Code Review Process

### For Contributors

- Address all feedback
- Update documentation
- Ensure tests pass
- Maintain backwards compatibility

### For Reviewers

- Check functionality
- Verify code style
- Test changes locally
- Review documentation updates

## Release Process

1. **Version Bump** in `pyproject.toml`
2. **Update CHANGELOG** with changes
3. **Tag Release** with semantic version
4. **Update Documentation** as needed

## Questions?

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check existing docs first

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a welcoming environment

Thank you for contributing to Everything DB Manager! 🚀
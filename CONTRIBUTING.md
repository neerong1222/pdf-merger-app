# Contributing to PDF Merger App

Thank you for your interest in contributing! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Focus on constructive feedback
- Help others succeed

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/pdf-merger-app.git
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test thoroughly**
6. **Commit with clear messages**:
   ```bash
   git commit -m "Add feature: clear description"
   ```
7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Create a Pull Request**

## Development Setup

```bash
./setup.sh          # macOS/Linux
setup.bat           # Windows

# Activate environment
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate.bat   # Windows

# Run tests
pytest tests/

# Start dev server
python app.py
```

## Commit Message Guidelines

```
Type: Short summary (50 chars or less)

More detailed explanation of the change (if needed).
- Point 1
- Point 2

Fixes #123 (if applicable)
```

**Types**: feat, fix, docs, style, refactor, test, chore, perf, security

## Code Style

- Use PEP 8 for Python
- Use 4 spaces for indentation
- Max line length: 88 characters
- Write docstrings for functions

```python
def validate_pdf(file_path):
    """Validate that the file is a valid PDF.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        bool: True if valid PDF, False otherwise
    """
    pass
```

## Testing

- Write tests for new features
- Run tests before committing: `pytest tests/`
- Aim for >80% code coverage
- Test edge cases and error conditions

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Reference any related issues
6. Wait for code review
7. Address feedback
8. Squash commits if requested

## Reporting Issues

- Use GitHub Issues
- Provide clear title and description
- Include steps to reproduce
- Share error logs/screenshots
- Specify your environment (OS, Python version)

## Security Issues

⚠️ **Do NOT open public issues for security vulnerabilities**

Email: security@yourdomain.com with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if available)

## Documentation

- Update README.md for user-facing changes
- Update SECURITY.md for security changes
- Add docstrings to new functions
- Include code examples

## Performance

- Benchmark changes affecting merge speed
- Optimize file I/O operations
- Profile memory usage with large files
- Document performance implications

## Areas for Contribution

- **Features**: Compression, encryption, watermarks
- **UI/UX**: Better design, accessibility
- **Performance**: Faster merging, lower memory
- **Security**: Vulnerability fixes, hardening
- **Documentation**: Guides, examples, translations
- **Tests**: More test coverage, edge cases

## Questions?

- Check existing issues
- Open a discussion
- Comment on related PRs
- Email: help@yourdomain.com

---

**Last Updated:** November 2024

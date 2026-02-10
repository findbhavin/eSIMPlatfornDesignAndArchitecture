# Contributing to eSim Platform Design and Architecture

Thank you for your interest in contributing to this project! This guide will help you get started.

## Code of Conduct

This project is part of the eSim Semester Long Internship program. All contributors are expected to:
- Be respectful and constructive
- Follow eSim community guidelines
- Write clean, documented code
- Include tests for new features

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest pytest-cov black flake8 mypy
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/your-bugfix-name
```

## Development Guidelines

### Code Style

- Follow **PEP 8** Python style guide
- Use **black** for code formatting: `black src/ tests/`
- Use **flake8** for linting: `flake8 src/ tests/`
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Testing

- Write tests for all new features
- Ensure all tests pass: `pytest`
- Aim for >90% code coverage
- Run tests before committing: `pytest -v`

### Documentation

- Update README.md if adding features
- Add docstrings to all public APIs
- Update USER_GUIDE.md for user-facing changes
- Update CHANGELOG.md with your changes

## Making Changes

### 1. Write Code

```python
# Add your feature or fix
# Follow existing code patterns
# Include docstrings and type hints
```

### 2. Write Tests

```python
# In tests/test_your_module.py
class TestYourFeature:
    def test_your_feature(self):
        """Test that your feature works."""
        assert your_feature() == expected_result
```

### 3. Run Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_your_module.py

# With coverage
pytest --cov=src --cov-report=html
```

### 4. Format Code

```bash
# Format with black
black src/ tests/

# Check with flake8
flake8 src/ tests/
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: Add your feature description"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: Add voltage analysis to CircuitAnalyzer

- Implement voltage node analysis
- Add tests for voltage calculations
- Update documentation

Closes #42
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (black)
- [ ] No linting errors (flake8)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] CHANGELOG.md updated
```

### Review Process

1. Maintainers will review your PR
2. Address any feedback
3. Once approved, PR will be merged

## What to Contribute

### Ideas for Contributions

#### Features
- Additional circuit analysis algorithms
- Enhanced simulation output parsing
- Visualization tools for results
- Additional example circuits
- Performance optimizations

#### Documentation
- More examples and tutorials
- API documentation improvements
- Translation to other languages
- Video tutorials

#### Testing
- Additional test cases
- Integration tests
- Performance benchmarks

#### Bug Fixes
- Check the issue tracker
- Fix reported bugs
- Improve error handling

## Reporting Issues

### Bug Reports

Create an issue with:
- Clear title
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Error messages/logs

**Template**:
```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: Ubuntu 20.04
- Python: 3.9
- eSim: 2.3

**Additional Context**
Any other relevant information
```

### Feature Requests

Create an issue with:
- Clear title
- Problem you're trying to solve
- Proposed solution
- Alternative solutions considered
- Additional context

## Questions?

- Check existing documentation in `docs/`
- Search existing issues
- Ask on the issue tracker
- Contact: contact-esim@fossee.in

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions help make this project better for everyone in the eSim community!

---

**eSim Semester Long Internship Spring 2026**  
*Empowering Open Source EDA Tools*

# Development Documentation

## Development Environment Setup

### Prerequisites Installation

#### 1. System Requirements
- **Operating System**: Linux (Ubuntu 20.04+), Windows 10+, or macOS 10.14+
- **RAM**: Minimum 4GB, Recommended 8GB
- **Disk Space**: 2GB for eSim + 1GB for project

#### 2. Install Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python3

# Windows
# Download from https://www.python.org/downloads/
```

Verify installation:
```bash
python3 --version  # Should be 3.7 or higher
pip3 --version
```

#### 3. Install eSim

**Ubuntu/Debian**:
```bash
# Download from https://esim.fossee.in/downloads
wget https://static.fossee.in/esim/installation-files/eSim-2.3.run
chmod +x eSim-2.3.run
./eSim-2.3.run
```

**Windows**:
- Download installer from https://esim.fossee.in/downloads
- Run the installer and follow instructions

**Verify**:
```bash
which ngspice
ngspice --version
```

#### 4. Install Git
```bash
# Ubuntu/Debian
sudo apt install git

# macOS
brew install git

# Windows
# Download from https://git-scm.com/download/win
```

### Project Setup

#### 1. Clone Repository
```bash
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

#### 4. Verify Installation
```bash
# Run tests
pytest tests/ -v

# Check code style
flake8 src/

# Run type checking
mypy src/
```

## Development Workflow

### 1. Branch Strategy

```
main (production)
  ├── develop (integration)
  │   ├── feature/circuit-analyzer
  │   ├── feature/esim-wrapper
  │   └── feature/config-manager
  └── hotfix/urgent-fix
```

**Branch Naming Conventions**:
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Urgent fixes
- `docs/description` - Documentation updates

### 2. Development Cycle

#### Step 1: Create Feature Branch
```bash
git checkout -b feature/my-feature
```

#### Step 2: Make Changes
```bash
# Edit files
# Run tests frequently
pytest tests/

# Check code style
black src/
flake8 src/
```

#### Step 3: Commit Changes
```bash
git add .
git commit -m "Add feature: description of changes"
```

**Commit Message Format**:
```
<type>: <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat: Add circuit validation to analyzer

- Implement validate_circuit() method
- Check for ground nodes
- Add comprehensive error messages

Closes #123
```

#### Step 4: Push and Create PR
```bash
git push origin feature/my-feature
# Create Pull Request on GitHub
```

### 3. Code Review Process

**Before Submitting PR**:
- [ ] All tests pass
- [ ] Code is formatted (black)
- [ ] No linting errors (flake8)
- [ ] Documentation updated
- [ ] Changelog updated

**PR Review Checklist**:
- [ ] Code follows project style
- [ ] Tests are comprehensive
- [ ] Documentation is clear
- [ ] No unnecessary changes
- [ ] Commits are well-organized

## Coding Standards

### Python Style Guide

Follow **PEP 8** guidelines with these specifics:

#### Naming Conventions
```python
# Classes: PascalCase
class CircuitAnalyzer:
    pass

# Functions and methods: snake_case
def analyze_circuit():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_TIMEOUT = 30

# Private methods: _leading_underscore
def _internal_method():
    pass
```

#### Docstrings
Use Google-style docstrings:
```python
def analyze_circuit(netlist_path: str, verbose: bool = False) -> Dict:
    """
    Analyze a circuit from netlist file.
    
    Args:
        netlist_path: Path to the netlist file
        verbose: Enable verbose output
        
    Returns:
        Dict containing analysis results with keys:
        - circuit_name: Name of the circuit
        - components: List of components
        - nodes: List of nodes
        
    Raises:
        FileNotFoundError: If netlist file doesn't exist
        ValueError: If netlist format is invalid
        
    Example:
        >>> analyzer = CircuitAnalyzer()
        >>> results = analyzer.analyze_circuit('circuit.cir')
        >>> print(results['circuit_name'])
    """
    pass
```

#### Type Hints
```python
from typing import Dict, List, Optional, Tuple

def process_data(
    input_file: str,
    options: Optional[Dict[str, Any]] = None
) -> Tuple[bool, List[str]]:
    """Process data with type hints."""
    pass
```

#### Code Formatting
```python
# Use black for automatic formatting
black src/ tests/

# Line length: 88 characters (black default)
# Indentation: 4 spaces
# String quotes: Double quotes preferred
```

### Testing Standards

#### Test Structure
```python
class TestCircuitAnalyzer:
    """Test suite for CircuitAnalyzer class."""
    
    def setup_method(self):
        """Set up test fixtures before each test."""
        self.analyzer = CircuitAnalyzer()
        
    def teardown_method(self):
        """Clean up after each test."""
        pass
        
    def test_initialization(self):
        """Test that analyzer initializes correctly."""
        assert self.analyzer is not None
        assert self.analyzer.components == {}
```

#### Test Naming
```python
def test_<functionality>_<scenario>_<expected_result>():
    """Test that functionality works in scenario and produces expected result."""
    pass

# Examples:
def test_load_netlist_with_valid_file_returns_true():
    pass

def test_parse_netlist_with_empty_file_raises_error():
    pass
```

#### Test Coverage Goals
- **Minimum**: 80% coverage
- **Target**: 90%+ coverage
- **Critical paths**: 100% coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

## Project Tools

### 1. pytest (Testing)
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_circuit_analyzer.py

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_circuit_analyzer.py::TestCircuitAnalyzer::test_initialization

# Run with coverage
pytest --cov=src

# Run with markers
pytest -m "slow"
```

### 2. black (Code Formatting)
```bash
# Format all code
black src/ tests/

# Check without modifying
black --check src/

# Format specific file
black src/esim_platform/circuit_analyzer.py
```

### 3. flake8 (Linting)
```bash
# Lint all code
flake8 src/ tests/

# With specific settings
flake8 --max-line-length=88 --extend-ignore=E203 src/
```

### 4. mypy (Type Checking)
```bash
# Type check all code
mypy src/

# Strict mode
mypy --strict src/

# Ignore missing imports
mypy --ignore-missing-imports src/
```

### 5. pytest-cov (Coverage)
```bash
# Basic coverage
pytest --cov=src

# With HTML report
pytest --cov=src --cov-report=html

# With missing lines
pytest --cov=src --cov-report=term-missing
```

## Debugging

### 1. Python Debugger (pdb)
```python
import pdb

def problematic_function():
    x = 10
    pdb.set_trace()  # Breakpoint
    y = x * 2
    return y
```

**Common pdb commands**:
- `l` - List source code
- `n` - Next line
- `s` - Step into function
- `c` - Continue execution
- `p variable` - Print variable
- `q` - Quit debugger

### 2. VS Code Debugging

Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"]
        }
    ]
}
```

### 3. Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Performance Optimization

### Profiling
```python
import cProfile
import pstats

# Profile a function
profiler = cProfile.Profile()
profiler.enable()

# Your code here
analyzer.analyze_circuit()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10
```

### Memory Profiling
```bash
# Install memory_profiler
pip install memory_profiler

# Decorate function
@profile
def memory_intensive_function():
    pass

# Run with memory profiler
python -m memory_profiler script.py
```

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/ci.yml`:
```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black
        
    - name: Lint with flake8
      run: flake8 src/
      
    - name: Format check with black
      run: black --check src/
      
    - name: Test with pytest
      run: pytest --cov=src --cov-report=xml
      
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Troubleshooting

### Common Issues

#### Issue: Import errors
```bash
# Solution: Install package in development mode
pip install -e .
```

#### Issue: Tests fail locally but pass in CI
```bash
# Solution: Use same Python version
pyenv install 3.9.0
pyenv local 3.9.0
```

#### Issue: ngspice not found
```bash
# Solution: Add to PATH
export PATH=$PATH:/usr/local/bin

# Or set environment variable
export ESIM_NGSPICE_PATH=/path/to/ngspice
```

## Best Practices

### Code Quality
1. **DRY** - Don't Repeat Yourself
2. **KISS** - Keep It Simple, Stupid
3. **YAGNI** - You Aren't Gonna Need It
4. **SOLID** - Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion

### Git Best Practices
1. Commit early, commit often
2. Write meaningful commit messages
3. Keep commits atomic
4. Review your own code before pushing
5. Pull before you push

### Security Best Practices
1. Never commit secrets or credentials
2. Use environment variables for sensitive data
3. Validate all inputs
4. Keep dependencies updated
5. Follow principle of least privilege

## Resources

### Documentation
- **Python**: https://docs.python.org/3/
- **pytest**: https://docs.pytest.org/
- **ngspice**: http://ngspice.sourceforge.net/docs.html
- **eSim**: https://esim.fossee.in/resources

### Tools
- **VS Code**: https://code.visualstudio.com/
- **PyCharm**: https://www.jetbrains.com/pycharm/
- **Git**: https://git-scm.com/doc

### Learning Resources
- **Real Python**: https://realpython.com/
- **Python Testing**: https://realpython.com/pytest-python-testing/
- **Circuit Analysis**: https://www.allaboutcircuits.com/

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Author**: eSim Internship Spring 2026

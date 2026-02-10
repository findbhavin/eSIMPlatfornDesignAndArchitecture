# eSim Tool Manager

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)

A comprehensive **Automated Tool Manager** for eSim that handles tool installation, version management, updates/upgrades, configuration, dependency checking, and provides a user-friendly command-line interface.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Command Reference](#command-reference)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [References](#references)
- [License](#license)

## Overview

eSim Tool Manager is a Python-based automation tool designed to simplify the installation, configuration, and maintenance of tools required for eSim circuit simulation. It currently supports:

- **Ngspice**: Open-source SPICE circuit simulator
- **KiCad**: Open-source electronics design automation suite

The tool manager provides:
- Automated installation with OS detection
- Version management and updates
- Dependency checking and validation
- Configuration management
- Comprehensive logging
- User-friendly CLI with colored output

## Features

### 🚀 Installation Management
- Automatic OS detection (Linux, Windows, macOS)
- One-command tool installation
- Version checking and validation
- Support for both system-wide and local installations

### 🔄 Update System
- Check for available updates
- Automated update process
- Update all tools at once
- Detailed update history tracking
- Rollback capability (planned)

### ⚙️ Configuration Management
- Automatic PATH configuration
- Environment variable management
- Tool-specific settings
- Configuration backup and restore
- YAML-based configuration files

### 🔍 Dependency Checker
- Python version validation
- System dependency verification
- Package compatibility checking
- Clear reporting of missing dependencies
- Installation suggestions

### 💻 User Interface
- Interactive CLI using Click
- Colored terminal output
- Progress indicators
- Comprehensive help system
- Both CLI and interactive modes

## System Requirements

### Minimum Requirements
- **Python**: 3.7 or higher
- **Operating System**: Linux, macOS, or Windows
- **Disk Space**: 100MB for the tool manager + space for tools
- **Internet Connection**: Required for downloading tools (optional for offline mode)

### Python Dependencies
All Python dependencies are automatically installed:
- `requests>=2.28.0` - For HTTP requests
- `click>=8.1.0` - For CLI interface
- `colorama>=0.4.6` - For colored output
- `pyyaml>=6.0` - For configuration files
- `packaging>=21.0` - For version comparison

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture/tool_manager
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python main.py --help
```

You should see the help message with available commands.

## Quick Start

### 1. Check System Status

```bash
python main.py status --verbose
```

This will show:
- System information
- Installed tools
- Configuration status
- Dependency status

### 2. Check Dependencies

```bash
python main.py check --all
```

This verifies all required dependencies are installed.

### 3. Install a Tool

```bash
# Install Ngspice
python main.py install ngspice

# Install KiCad
python main.py install kicad

# Install specific version
python main.py install ngspice --version 40
```

### 4. List Installed Tools

```bash
python main.py list --verbose
```

### 5. Update Tools

```bash
# Update a specific tool
python main.py update ngspice

# Check for updates only
python main.py update ngspice --check-only

# Update all tools
python main.py update --all
```

## Usage

### Interactive Mode

For a menu-driven interface:

```bash
python main.py --interactive
```

This will display an interactive menu with all available options.

### Command-Line Mode

Use specific commands for automation:

```bash
# General format
python main.py <command> [options] [arguments]

# Examples
python main.py list
python main.py install ngspice
python main.py update --all
python main.py check kicad
```

## Command Reference

### `list` - List Installed Tools

```bash
python main.py list [--verbose]
```

**Options:**
- `--verbose, -v`: Show detailed information including update availability

**Example:**
```bash
python main.py list -v
```

### `install` - Install a Tool

```bash
python main.py install <tool> [--version VERSION] [--force]
```

**Arguments:**
- `tool`: Tool name (ngspice or kicad)

**Options:**
- `--version, -v`: Specific version to install (default: latest)
- `--force, -f`: Force reinstall even if already installed

**Examples:**
```bash
python main.py install ngspice
python main.py install kicad --version 7.0.0
python main.py install ngspice --force
```

### `update` - Update Tools

```bash
python main.py update [tool] [--all] [--check-only]
```

**Arguments:**
- `tool`: Tool name to update (optional if using --all)

**Options:**
- `--all, -a`: Update all installed tools
- `--check-only, -c`: Only check for updates without installing

**Examples:**
```bash
python main.py update ngspice
python main.py update --all
python main.py update kicad --check-only
```

### `check` - Check Dependencies

```bash
python main.py check [tool] [--all] [--verbose]
```

**Arguments:**
- `tool`: Specific tool to check (optional)

**Options:**
- `--all, -a`: Check all tools
- `--verbose, -v`: Show detailed report

**Examples:**
```bash
python main.py check --all
python main.py check ngspice --verbose
python main.py check python
```

### `config` - Configure Tools

```bash
python main.py config <tool> [options]
```

**Arguments:**
- `tool`: Tool name to configure

**Options:**
- `--enable/--disable`: Enable or disable the tool
- `--auto-update/--no-auto-update`: Enable or disable auto-updates
- `--path PATH`: Set the tool installation path

**Examples:**
```bash
python main.py config ngspice --enable --auto-update
python main.py config kicad --path /usr/local/bin/kicad
python main.py config ngspice  # Show current configuration
```

### `logs` - View Action Logs

```bash
python main.py logs [--limit N] [--tool TOOL]
```

**Options:**
- `--limit, -n`: Number of log entries to show (default: 10)
- `--tool`: Filter logs by tool name

**Examples:**
```bash
python main.py logs
python main.py logs --limit 20
python main.py logs --tool ngspice
```

### `status` - Show System Status

```bash
python main.py status [--verbose]
```

**Options:**
- `--verbose, -v`: Show detailed information

**Example:**
```bash
python main.py status -v
```

## Configuration

### Configuration File

The tool manager uses a YAML configuration file located at:
- Default: `tool_manager/config.yaml`
- User home: `~/.esim_tools/config.yaml`

### Configuration Structure

```yaml
system:
  os: linux
  python_version: "3.12"

tools:
  ngspice:
    enabled: true
    auto_update: false
    path: ""
    environment_vars:
      SPICE_LIB_DIR: ""
      SPICE_EXEC_DIR: ""
  
  kicad:
    enabled: true
    auto_update: false
    path: ""
    environment_vars:
      KICAD_SYMBOL_DIR: ""
      KICAD_FOOTPRINT_DIR: ""

paths:
  install_dir: ~/.esim_tools
  cache_dir: ~/.esim_tools/cache
  log_dir: ~/.esim_tools/logs

update:
  check_on_startup: true
  auto_install: false
  update_interval_days: 7

logging:
  level: INFO
  file_logging: true
  console_logging: true
```

### Editing Configuration

You can edit the configuration file directly or use the `config` command:

```bash
# View current configuration
python main.py config ngspice

# Modify configuration
python main.py config ngspice --enable --auto-update
```

### Configuration Backup

The tool manager automatically creates backups in `tool_manager/config_backups/` before making changes.

## Troubleshooting

### Common Issues

#### 1. Python Version Error

**Error:** `Python 3.7+ is required`

**Solution:**
```bash
# Check your Python version
python3 --version

# Use Python 3.7 or higher
python3.8 -m venv venv
```

#### 2. Permission Denied During Installation

**Error:** `Permission denied` or `Access denied`

**Solution:**
```bash
# On Linux/macOS, you may need sudo for system-wide installation
sudo python main.py install ngspice

# Or use local installation (recommended)
python main.py install ngspice --path ~/.local/bin
```

#### 3. Tool Not Found After Installation

**Issue:** Tool installed but not found in PATH

**Solution:**
```bash
# Add tool to PATH manually
export PATH="$HOME/.local/bin:$PATH"

# Or let the tool manager configure it
python main.py config ngspice --path ~/.local/bin/ngspice
```

#### 4. Dependency Check Fails

**Issue:** Missing system dependencies

**Solution:**
```bash
# Check what's missing
python main.py check --all --verbose

# Install system dependencies
# On Ubuntu/Debian:
sudo apt-get install libx11-dev libreadline-dev

# On macOS:
brew install libx11 readline
```

#### 5. Update Check Fails

**Issue:** Cannot check for updates

**Solution:**
- Ensure you have internet connection
- Check if firewall is blocking requests
- Try manual update from official websites

### Getting Help

1. **Check Logs:**
   ```bash
   python main.py logs --limit 50
   ```

2. **View Detailed Status:**
   ```bash
   python main.py status --verbose
   ```

3. **Run Dependency Check:**
   ```bash
   python main.py check --all --verbose
   ```

4. **Check Configuration:**
   ```bash
   python main.py config ngspice
   ```

### Debug Mode

For more detailed logging, set the log level in your configuration:

```yaml
logging:
  level: DEBUG
```

Or set environment variable:
```bash
export LOG_LEVEL=DEBUG
python main.py status
```

## Testing

### Running Tests

Basic unit tests are provided in the `tests/` directory:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_tool_manager.py::test_installation
```

### Manual Testing

Test the tool manager functionality:

```bash
# 1. Test dependency checking
python main.py check --all

# 2. Test listing (before installation)
python main.py list

# 3. Test installation
python main.py install ngspice

# 4. Test configuration
python main.py config ngspice --enable

# 5. Test update checking
python main.py update ngspice --check-only

# 6. Test logging
python main.py logs

# 7. Test status
python main.py status --verbose
```

## Architecture

### Module Structure

```
tool_manager/
├── main.py              # Entry point and initialization
├── installation.py      # Tool installation management
├── update.py           # Update and upgrade system
├── config.py           # Configuration handling
├── dependency.py       # Dependency checker
├── interface.py        # CLI user interface
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── config.yaml        # Configuration file (generated)
├── logs/              # Log files directory
│   └── updates.json   # Update history
└── config_backups/    # Configuration backups
```

### Design Principles

1. **Modularity**: Each module has a specific responsibility
2. **Extensibility**: Easy to add new tools
3. **Error Handling**: Comprehensive error handling throughout
4. **Logging**: Detailed logging for debugging
5. **User-Friendly**: Clear messages and colored output

## Contributing

This project is part of the eSim Semester Long Internship. To contribute:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature
   ```
3. **Make your changes**
4. **Write tests** for new functionality
5. **Update documentation**
6. **Commit your changes:**
   ```bash
   git commit -m "Add your feature"
   ```
7. **Push to your fork:**
   ```bash
   git push origin feature/your-feature
   ```
8. **Create a Pull Request**

### Coding Standards

- Follow PEP 8 style guide
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new features
- Update README for new commands or features

## References

### Official Resources

- **eSim Official Website**: https://esim.fossee.in/
  - The main eSim project website with downloads and documentation
  
- **Ngspice**: http://ngspice.sourceforge.net/
  - Open-source SPICE circuit simulator
  - Download: http://ngspice.sourceforge.net/download.html
  - Documentation: http://ngspice.sourceforge.net/docs.html
  
- **KiCad**: https://www.kicad.org/
  - Open-source electronics design automation suite
  - Download: https://www.kicad.org/download/
  - Documentation: https://docs.kicad.org/

### Python Libraries

- **argparse**: https://docs.python.org/3/library/argparse.html
  - Command-line argument parsing
  
- **click**: https://click.palletsprojects.com/
  - Python command-line interface creation kit
  
- **colorama**: https://pypi.org/project/colorama/
  - Cross-platform colored terminal output

### Related Documentation

- **eSim Resources**: https://esim.fossee.in/resources
- **Circuit Simulation Procedure**: https://esim.fossee.in/circuit-simulation-project/procedure
- **FOSSEE**: https://fossee.in/

## Evaluator Access

Repository access has been granted to: https://github.com/Eyantra698Sumanto

## License

This project is developed as part of the eSim Semester Long Internship Spring 2026.

See the [LICENSE](../LICENSE) file for details.

## Acknowledgments

- **FOSSEE Team** for developing and maintaining eSim
- **eSim Community** for support and resources
- **Ngspice Team** for the circuit simulation engine
- **KiCad Team** for the electronics design suite

---

**eSim Semester Long Internship Spring 2026**  
*Empowering Open Source EDA Tools*

## Quick Command Cheat Sheet

```bash
# Installation
python main.py install ngspice
python main.py install kicad

# List tools
python main.py list -v

# Update
python main.py update ngspice
python main.py update --all

# Check dependencies
python main.py check --all

# Configure
python main.py config ngspice --enable

# View logs
python main.py logs -n 20

# Status
python main.py status -v

# Interactive mode
python main.py --interactive
```

For more help on any command:
```bash
python main.py <command> --help
```

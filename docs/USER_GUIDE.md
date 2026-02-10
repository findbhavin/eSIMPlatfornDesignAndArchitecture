# User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Using Circuit Analyzer](#using-circuit-analyzer)
4. [Using eSim Wrapper](#using-esim-wrapper)
5. [Configuration Management](#configuration-management)
6. [Working with Circuits](#working-with-circuits)
7. [Examples and Tutorials](#examples-and-tutorials)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

## Introduction

Welcome to the eSim Platform Design and Architecture project! This guide will help you get started with analyzing circuits, running simulations, and integrating with the eSim platform.

### What Can You Do?

- ✅ Analyze SPICE netlist files
- ✅ Run circuit simulations with eSim/ngspice
- ✅ Manage configuration easily
- ✅ Access example circuits
- ✅ Integrate eSim into Python workflows

## Getting Started

### Installation

#### Step 1: Install Prerequisites

**Python 3.7+**:
```bash
# Check if Python is installed
python3 --version

# If not installed:
# Ubuntu/Debian
sudo apt install python3 python3-pip

# macOS
brew install python3

# Windows: Download from https://www.python.org/downloads/
```

**eSim**:
- Download from: https://esim.fossee.in/downloads
- Follow installation instructions for your OS
- Verify: `ngspice --version`

#### Step 2: Install the Project

```bash
# Clone repository
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Verify Installation

```bash
# Run tests
pytest tests/ -v

# Should see all tests passing ✓
```

### Quick Start Example

```python
# Import modules
from src.esim_platform import CircuitAnalyzer, ESimWrapper

# Analyze a circuit
analyzer = CircuitAnalyzer()
analyzer.load_netlist('circuits/voltage_divider.cir')
analyzer.parse_netlist()
results = analyzer.analyze_circuit()

print(f"Circuit: {results['circuit_name']}")
print(f"Components: {results['total_components']}")
print(f"Nodes: {results['total_nodes']}")

# Run simulation
wrapper = ESimWrapper()
success, output = wrapper.simulate_circuit('circuits/voltage_divider.cir')
if success:
    print("Simulation completed!")
```

## Using Circuit Analyzer

The `CircuitAnalyzer` class helps you parse and analyze SPICE netlist files.

### Basic Usage

#### 1. Create an Analyzer Instance

```python
from src.esim_platform import CircuitAnalyzer

analyzer = CircuitAnalyzer()
```

Or initialize with a netlist path:
```python
analyzer = CircuitAnalyzer('/path/to/circuit.cir')
```

#### 2. Load a Netlist

```python
# Load from file
success = analyzer.load_netlist('circuits/voltage_divider.cir')

if success:
    print("Netlist loaded successfully!")
else:
    print("Failed to load netlist")
```

#### 3. Parse the Netlist

```python
# Parse the loaded netlist
circuit_info = analyzer.parse_netlist()

print(f"Circuit Name: {circuit_info['circuit_name']}")
print(f"Number of Components: {circuit_info['component_count']}")
print(f"Number of Nodes: {circuit_info['node_count']}")
```

#### 4. Analyze the Circuit

```python
# Perform comprehensive analysis
analysis = analyzer.analyze_circuit()

# Access analysis results
print(f"Total Components: {analysis['total_components']}")
print(f"Total Nodes: {analysis['total_nodes']}")
print(f"Component Summary: {analysis['component_summary']}")

# Component summary shows count by type
# Example: {'R': 2, 'V': 1, 'C': 1}
```

#### 5. Validate the Circuit

```python
# Check for common issues
is_valid, issues = analyzer.validate_circuit()

if is_valid:
    print("Circuit is valid!")
else:
    print("Circuit has issues:")
    for issue in issues:
        print(f"  - {issue}")
```

#### 6. Get Component Summary

```python
# Get count of each component type
summary = analyzer.get_component_summary()

for comp_type, count in summary.items():
    print(f"{comp_type}: {count}")
# Output:
# R: 2  (2 resistors)
# V: 1  (1 voltage source)
```

### Complete Example

```python
from src.esim_platform import CircuitAnalyzer

def analyze_my_circuit(circuit_file):
    """Analyze a circuit and print detailed information."""
    
    # Create analyzer
    analyzer = CircuitAnalyzer()
    
    # Load netlist
    if not analyzer.load_netlist(circuit_file):
        print(f"Error: Could not load {circuit_file}")
        return
    
    # Parse netlist
    info = analyzer.parse_netlist()
    
    # Display basic information
    print("=" * 50)
    print(f"Circuit Analysis: {info['circuit_name']}")
    print("=" * 50)
    print(f"Components: {info['component_count']}")
    print(f"Nodes: {info['node_count']}")
    print()
    
    # Show component breakdown
    summary = analyzer.get_component_summary()
    print("Component Summary:")
    for comp_type, count in summary.items():
        type_names = {
            'R': 'Resistors',
            'C': 'Capacitors',
            'L': 'Inductors',
            'V': 'Voltage Sources',
            'I': 'Current Sources',
            'D': 'Diodes'
        }
        name = type_names.get(comp_type, comp_type)
        print(f"  {name}: {count}")
    print()
    
    # Validate circuit
    is_valid, issues = analyzer.validate_circuit()
    if is_valid:
        print("✓ Circuit validation passed")
    else:
        print("⚠ Circuit has issues:")
        for issue in issues:
            print(f"  - {issue}")

# Use it
analyze_my_circuit('circuits/rc_filter.cir')
```

## Using eSim Wrapper

The `ESimWrapper` class provides an interface to run simulations using eSim/ngspice.

### Basic Usage

#### 1. Create a Wrapper Instance

```python
from src.esim_platform import ESimWrapper

# Create wrapper (auto-detects eSim installation)
wrapper = ESimWrapper()

# Or specify eSim path
wrapper = ESimWrapper('/path/to/esim')
```

#### 2. Check eSim Availability

```python
if wrapper.is_esim_available():
    print("eSim/ngspice is available!")
else:
    print("eSim/ngspice not found. Please install it.")
```

#### 3. Run a Simulation

```python
# Simulate a circuit
success, output = wrapper.simulate_circuit('circuits/voltage_divider.cir')

if success:
    print("Simulation completed successfully!")
    print("Output:")
    print(output)
else:
    print("Simulation failed:")
    print(output)  # Contains error message
```

#### 4. Parse Simulation Output

```python
# Run simulation
success, output = wrapper.simulate_circuit('circuits/rc_filter.cir')

if success:
    # Parse the output
    info = wrapper.parse_simulation_output(output)
    
    print(f"Success: {info['success']}")
    print(f"Errors: {len(info['errors'])}")
    print(f"Warnings: {len(info['warnings'])}")
    
    if info['errors']:
        print("Errors found:")
        for error in info['errors']:
            print(f"  - {error}")
```

#### 5. Get Wrapper Status

```python
# Get information about the wrapper
status = wrapper.get_simulation_status()

print(f"eSim Path: {status['esim_path']}")
print(f"Available: {status['esim_available']}")
print(f"Simulations Run: {status['simulations_run']}")
```

### Complete Example

```python
from src.esim_platform import ESimWrapper

def run_circuit_simulation(circuit_file):
    """Run simulation and display results."""
    
    # Create wrapper
    wrapper = ESimWrapper()
    
    # Check availability
    if not wrapper.is_esim_available():
        print("Error: ngspice not found. Please install eSim.")
        return
    
    print(f"Simulating: {circuit_file}")
    print("-" * 50)
    
    # Run simulation
    success, output = wrapper.simulate_circuit(circuit_file)
    
    if success:
        print("✓ Simulation completed successfully")
        
        # Parse output
        info = wrapper.parse_simulation_output(output)
        
        # Show warnings if any
        if info['warnings']:
            print(f"\n⚠ Warnings ({len(info['warnings'])}):")
            for warning in info['warnings']:
                print(f"  {warning}")
        
        # Show simulation output
        print("\nSimulation Output:")
        print(output[:500])  # First 500 characters
        
    else:
        print("✗ Simulation failed")
        print("\nError Details:")
        print(output)

# Use it
run_circuit_simulation('circuits/voltage_divider.cir')
```

### Creating Simple Netlists

```python
from src.esim_platform import ESimWrapper

wrapper = ESimWrapper()

# Create a voltage divider netlist
netlist = wrapper.create_simple_netlist('voltage_divider')
print(netlist)

# Create an RC filter netlist
netlist = wrapper.create_simple_netlist('rc_filter')
print(netlist)

# Save to file
with open('my_circuit.cir', 'w') as f:
    f.write(netlist)
```

## Configuration Management

The `ConfigManager` class handles application configuration.

### Basic Usage

#### 1. Create Configuration Manager

```python
from src.esim_platform import ConfigManager

# Create with default configuration
config = ConfigManager()

# Or load from file
config = ConfigManager('my_config.yaml')
```

#### 2. Get Configuration Values

```python
# Get with dot notation
timeout = config.get('esim.timeout')
output_dir = config.get('simulation.output_dir')

# Get with default value
custom_value = config.get('custom.key', 'default_value')
```

#### 3. Set Configuration Values

```python
# Set values
config.set('esim.timeout', 60)
config.set('simulation.verbosity', 'verbose')
config.set('new.nested.key', 'value')
```

#### 4. Save Configuration

```python
# Save to file
config.save_to_file('my_config.yaml')
```

#### 5. Get All Configuration

```python
# Get entire configuration dictionary
all_config = config.get_all()

import json
print(json.dumps(all_config, indent=2))
```

### Configuration File Format

Create `config.yaml`:
```yaml
esim:
  installation_path: /usr/share/esim
  ngspice_path: /usr/bin/ngspice
  timeout: 30

simulation:
  output_dir: ./simulation_results
  keep_intermediate_files: false
  verbosity: normal

circuit:
  default_ground: '0'
  default_temp: 27
  default_precision: 1e-6
```

### Environment Variables

Set environment variables (override config file):
```bash
export ESIM_INSTALLATION_PATH=/custom/esim/path
export ESIM_TIMEOUT=60
export ESIM_OUTPUT_DIR=/tmp/simulations
```

Then in Python:
```python
config = ConfigManager()
# Will automatically load from environment variables
```

### Complete Example

```python
from src.esim_platform import ConfigManager

# Create configuration
config = ConfigManager()

# Customize settings
config.set('esim.timeout', 90)
config.set('simulation.output_dir', './my_results')
config.set('simulation.verbosity', 'verbose')

# Save configuration
config.save_to_file('my_config.yaml')

# Later, load it back
new_config = ConfigManager('my_config.yaml')
print(f"Timeout: {new_config.get('esim.timeout')}")  # 90
```

## Working with Circuits

### Running Example Circuits

The project includes four example circuits:

#### 1. Voltage Divider

```bash
# Using ngspice directly
ngspice circuits/voltage_divider.cir

# Using Python
python3 -c "
from src.esim_platform import ESimWrapper
w = ESimWrapper()
success, output = w.simulate_circuit('circuits/voltage_divider.cir')
print(output if success else 'Failed')
"
```

#### 2. RC Filter

```bash
ngspice circuits/rc_filter.cir
```

Expected output: Frequency response showing -3dB cutoff at ~159 Hz

#### 3. Op-Amp (Non-Inverting)

```bash
ngspice circuits/opamp_noninverting.cir
```

Expected output: Voltage gain of 11 (20.8 dB)

#### 4. Half-Wave Rectifier

```bash
ngspice circuits/rectifier.cir
```

Expected output: AC to DC conversion with ripple

### Creating Your Own Circuit

1. **Create a netlist file** (`my_circuit.cir`):
```spice
* My First Circuit
.title Test Circuit

V1 1 0 DC 5V
R1 1 2 1k
R2 2 0 1k

.op
.end
```

2. **Analyze it**:
```python
from src.esim_platform import CircuitAnalyzer

analyzer = CircuitAnalyzer()
analyzer.load_netlist('my_circuit.cir')
analyzer.parse_netlist()
results = analyzer.analyze_circuit()
print(results)
```

3. **Simulate it**:
```python
from src.esim_platform import ESimWrapper

wrapper = ESimWrapper()
success, output = wrapper.simulate_circuit('my_circuit.cir')
print(output)
```

## Examples and Tutorials

### Tutorial 1: Analyze Multiple Circuits

```python
from src.esim_platform import CircuitAnalyzer
import glob

def analyze_all_circuits(pattern='circuits/*.cir'):
    """Analyze all circuits matching pattern."""
    
    analyzer = CircuitAnalyzer()
    
    for circuit_file in glob.glob(pattern):
        print(f"\n{'='*60}")
        print(f"Analyzing: {circuit_file}")
        print('='*60)
        
        if analyzer.load_netlist(circuit_file):
            analyzer.parse_netlist()
            analysis = analyzer.analyze_circuit()
            
            print(f"Circuit: {analysis['circuit_name']}")
            print(f"Components: {analysis['total_components']}")
            print(f"Nodes: {analysis['total_nodes']}")
            
            summary = analysis['component_summary']
            print("Components:", ', '.join(f"{k}={v}" for k, v in summary.items()))

# Run it
analyze_all_circuits()
```

### Tutorial 2: Batch Simulation

```python
from src.esim_platform import ESimWrapper
import glob
import os

def run_batch_simulations(pattern='circuits/*.cir', output_dir='results'):
    """Run simulations on multiple circuits."""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    wrapper = ESimWrapper()
    
    if not wrapper.is_esim_available():
        print("Error: ngspice not available")
        return
    
    results = {}
    
    for circuit_file in glob.glob(pattern):
        circuit_name = os.path.basename(circuit_file)
        print(f"\nSimulating: {circuit_name}")
        
        success, output = wrapper.simulate_circuit(circuit_file)
        results[circuit_name] = success
        
        # Save output
        output_file = os.path.join(output_dir, f"{circuit_name}.out")
        with open(output_file, 'w') as f:
            f.write(output)
        
        status = "✓" if success else "✗"
        print(f"  {status} {'Success' if success else 'Failed'}")
    
    # Summary
    print("\n" + "="*60)
    print("Simulation Summary:")
    print("="*60)
    success_count = sum(1 for s in results.values() if s)
    total_count = len(results)
    print(f"Successful: {success_count}/{total_count}")
    
    return results

# Run it
run_batch_simulations()
```

### Tutorial 3: Complete Workflow

```python
from src.esim_platform import CircuitAnalyzer, ESimWrapper, ConfigManager

def complete_circuit_workflow(circuit_file):
    """Complete workflow: configure, analyze, simulate."""
    
    print("="*70)
    print(f"Processing: {circuit_file}")
    print("="*70)
    
    # 1. Load configuration
    config = ConfigManager()
    config.set('esim.timeout', 60)
    print("\n1. Configuration loaded")
    
    # 2. Analyze circuit
    print("\n2. Analyzing circuit...")
    analyzer = CircuitAnalyzer()
    
    if not analyzer.load_netlist(circuit_file):
        print("   Error loading netlist")
        return
    
    analyzer.parse_netlist()
    analysis = analyzer.analyze_circuit()
    
    print(f"   Circuit: {analysis['circuit_name']}")
    print(f"   Components: {analysis['total_components']}")
    print(f"   Nodes: {analysis['total_nodes']}")
    
    # 3. Validate circuit
    print("\n3. Validating circuit...")
    is_valid, issues = analyzer.validate_circuit()
    
    if is_valid:
        print("   ✓ Validation passed")
    else:
        print("   ⚠ Issues found:")
        for issue in issues:
            print(f"     - {issue}")
    
    # 4. Run simulation
    print("\n4. Running simulation...")
    wrapper = ESimWrapper()
    
    if not wrapper.is_esim_available():
        print("   ⚠ ngspice not available, skipping simulation")
        return
    
    success, output = wrapper.simulate_circuit(circuit_file)
    
    if success:
        print("   ✓ Simulation completed")
        
        # Parse output
        info = wrapper.parse_simulation_output(output)
        if info['warnings']:
            print(f"   ⚠ {len(info['warnings'])} warnings")
    else:
        print("   ✗ Simulation failed")
    
    print("\n" + "="*70)
    print("Workflow completed")
    print("="*70)

# Run complete workflow
complete_circuit_workflow('circuits/voltage_divider.cir')
```

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "ngspice not found"

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install ngspice

# macOS
brew install ngspice

# Or install eSim which includes ngspice
# Download from https://esim.fossee.in/downloads
```

#### Issue 2: "Module not found" errors

**Solution**:
```bash
# Make sure you're in the project directory
cd eSIMPlatfornDesignAndArchitecture

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Issue 3: Import errors

**Solution**:
```bash
# Add project to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or install in development mode
pip install -e .
```

#### Issue 4: Simulation timeout

**Solution**:
```python
# Increase timeout in configuration
config = ConfigManager()
config.set('esim.timeout', 120)  # 120 seconds
```

#### Issue 5: Permission errors

**Solution**:
```bash
# Make sure you have write permissions
chmod +w simulation_results/

# Or change output directory
config.set('simulation.output_dir', '/tmp/simulations')
```

## FAQ

### Q1: Do I need eSim installed?

**A**: For circuit analysis (parsing netlists), no. For running simulations, you need ngspice (usually included with eSim).

### Q2: Can I use this on Windows?

**A**: Yes! The Python modules work on Windows. You'll need to install:
- Python 3.7+
- eSim for Windows (includes ngspice)

### Q3: What circuit formats are supported?

**A**: The analyzer supports SPICE netlist format (.cir, .sp, .net files). These are standard files used by ngspice and eSim.

### Q4: Can I create circuits programmatically?

**A**: Yes! Use the `create_simple_netlist()` method or write netlist strings directly:

```python
netlist = """* My Circuit
V1 1 0 DC 10V
R1 1 0 1k
.op
.end
"""

with open('my_circuit.cir', 'w') as f:
    f.write(netlist)
```

### Q5: How do I visualize simulation results?

**A**: Use matplotlib to plot results from simulation output, or use eSim's built-in plotting tools via the GUI.

### Q6: Are there more example circuits?

**A**: The project includes 4 example circuits. You can find more at:
- https://esim.fossee.in/circuit-simulation-project/procedure
- ngspice examples directory

### Q7: Can I contribute circuits?

**A**: Yes! Follow the contribution guidelines and submit a PR with your circuit designs.

### Q8: How do I report bugs?

**A**: Create an issue on GitHub: https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture/issues

## Additional Resources

- **eSim Documentation**: https://esim.fossee.in/resources
- **ngspice Manual**: http://ngspice.sourceforge.net/docs.html
- **SPICE Tutorial**: https://www.allaboutcircuits.com/textbook/reference/chpt-7/example-circuits-and-netlists/
- **Project Documentation**: See `docs/` directory

## Getting Help

Need help? Here's where to get support:

1. **Documentation**: Check docs/ directory
2. **Examples**: See examples/ directory
3. **Issues**: https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture/issues
4. **eSim Support**: contact-esim@fossee.in

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Author**: eSim Internship Spring 2026

Happy Simulating! 🔌⚡

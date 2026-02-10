# eSim Platform Design and Architecture

[![eSim](https://img.shields.io/badge/eSim-Circuit%20Simulation-blue)](https://esim.fossee.in/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project is part of the **eSim Semester Long Internship Spring 2026** assignment, providing a comprehensive integration platform for eSim (Electronic Simulation Tool). It includes software components for circuit analysis, simulation wrappers, configuration management, and example circuit designs.

eSim is an open-source EDA tool for circuit design, simulation, and PCB design. This project extends eSim's capabilities with Python-based tools for automation and analysis.

## Features

- **Circuit Analysis**: Parse and analyze SPICE netlists
- **eSim Integration**: Wrapper for eSim/ngspice simulation execution
- **Configuration Management**: Flexible configuration system with YAML and environment variable support
- **Example Circuits**: Collection of standard circuit designs (Op-Amp, filters, rectifiers)
- **Comprehensive Testing**: Full test suite with pytest
- **Well-Documented**: Extensive documentation and inline code comments

## Project Structure

```
eSIMPlatfornDesignAndArchitecture/
├── src/
│   └── esim_platform/          # Core Python modules
│       ├── __init__.py
│       ├── circuit_analyzer.py  # Circuit analysis tools
│       ├── esim_wrapper.py      # eSim simulation wrapper
│       └── config_manager.py    # Configuration management
├── circuits/                    # Example circuit designs
│   ├── opamp_noninverting.cir
│   ├── rc_filter.cir
│   ├── voltage_divider.cir
│   └── rectifier.cir
├── tests/                       # Unit tests
│   ├── test_circuit_analyzer.py
│   ├── test_esim_wrapper.py
│   └── test_config_manager.py
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md
│   ├── CIRCUIT_DESIGN.md
│   ├── DEVELOPMENT.md
│   └── USER_GUIDE.md
├── examples/                    # Example usage scripts
│   └── sample_circuits/
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md                    # This file
```

## Prerequisites

- **Python**: 3.7 or higher
- **eSim**: Installed from [esim.fossee.in](https://esim.fossee.in/downloads)
- **ngspice**: Circuit simulator (usually included with eSim)
- **Git**: For version control

### Optional
- **PySpice**: For advanced circuit simulation features
- **matplotlib**: For plotting simulation results

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture
```

### 2. Set Up Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install eSim

Download and install eSim from the official website:
- **Website**: https://esim.fossee.in/downloads
- **Documentation**: https://esim.fossee.in/resources

Follow the installation instructions for your operating system.

### 5. Verify Installation

```bash
# Check if ngspice is available
which ngspice

# Run tests
pytest tests/
```

## Quick Start

### Using the Circuit Analyzer

```python
from src.esim_platform import CircuitAnalyzer

# Create analyzer instance
analyzer = CircuitAnalyzer()

# Load and parse a netlist
analyzer.load_netlist('circuits/voltage_divider.cir')
analyzer.parse_netlist()

# Analyze the circuit
analysis = analyzer.analyze_circuit()
print(f"Circuit: {analysis['circuit_name']}")
print(f"Components: {analysis['total_components']}")
print(f"Nodes: {analysis['total_nodes']}")
```

### Using the eSim Wrapper

```python
from src.esim_platform import ESimWrapper

# Create wrapper instance
wrapper = ESimWrapper()

# Check if eSim is available
if wrapper.is_esim_available():
    # Run simulation
    success, output = wrapper.simulate_circuit('circuits/rc_filter.cir')
    if success:
        print("Simulation completed successfully!")
        print(output)
```

### Using Configuration Manager

```python
from src.esim_platform import ConfigManager

# Load configuration
config = ConfigManager('config.yaml')

# Get configuration values
timeout = config.get('esim.timeout', 30)
output_dir = config.get('simulation.output_dir')

# Set configuration values
config.set('esim.timeout', 60)
config.save_to_file('config.yaml')
```

## Circuit Examples

The project includes several standard circuit designs:

1. **Voltage Divider** (`circuits/voltage_divider.cir`)
   - Basic resistive voltage divider
   - DC analysis

2. **RC Low Pass Filter** (`circuits/rc_filter.cir`)
   - First-order passive filter
   - Frequency response analysis
   - Cutoff frequency: ~159 Hz

3. **Non-Inverting Op-Amp** (`circuits/opamp_noninverting.cir`)
   - Operational amplifier in non-inverting configuration
   - Voltage gain: 11
   - AC and transient analysis

4. **Half-Wave Rectifier** (`circuits/rectifier.cir`)
   - AC to DC conversion
   - With filtering capacitor
   - Transient analysis

### Running Circuit Simulations

```bash
# Using ngspice directly
ngspice circuits/voltage_divider.cir

# Using the Python wrapper
python3 -c "from src.esim_platform import ESimWrapper; \
            w = ESimWrapper(); \
            print(w.simulate_circuit('circuits/voltage_divider.cir'))"
```

## Testing

Run the complete test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_circuit_analyzer.py

# Run with verbose output
pytest -v
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System architecture and design decisions
- **[CIRCUIT_DESIGN.md](docs/CIRCUIT_DESIGN.md)**: Detailed circuit design documentation
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)**: Development guide and best practices
- **[USER_GUIDE.md](docs/USER_GUIDE.md)**: Step-by-step user guide with examples

## Contributing

This is an academic project for the eSim Semester Long Internship. For the internship program:

1. Follow the eSim coding standards
2. Write tests for new features
3. Update documentation
4. Follow Git best practices

## Resources

- **eSim Official Website**: https://esim.fossee.in/
- **eSim Downloads**: https://esim.fossee.in/downloads
- **eSim Resources**: https://esim.fossee.in/resources
- **Circuit Simulation Procedure**: https://esim.fossee.in/circuit-simulation-project/procedure
- **ngspice Manual**: http://ngspice.sourceforge.net/docs.html

## Contact

For questions or support:
- **eSim Team**: contact-esim@fossee.in
- **Repository Issues**: [GitHub Issues](https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture/issues)

## License

This project is developed as part of the eSim Semester Long Internship Spring 2026.

## Acknowledgments

- **FOSSEE Team** for developing and maintaining eSim
- **eSim Community** for support and resources
- **ngspice Team** for the circuit simulation engine

---

**eSim Semester Long Internship Spring 2026**  
*Empowering Open Source EDA Tools*

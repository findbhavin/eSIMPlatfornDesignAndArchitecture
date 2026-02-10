# eSim Platform Design and Architecture

[![eSim](https://img.shields.io/badge/eSim-Circuit%20Simulation-blue)](https://esim.fossee.in/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

This project is part of the **eSim Semester Long Internship Spring 2026** assignment, providing a comprehensive integration platform for eSim (Electronic Simulation Tool). It includes a modern web interface, REST API, backend Python modules for circuit analysis, simulation wrappers, configuration management, and example circuit designs.

eSim is an open-source EDA tool for circuit design, simulation, and PCB design. This project extends eSim's capabilities with a full-stack web application for automation and analysis.

## Features

### Backend
- **Circuit Analysis**: Parse and analyze SPICE netlists
- **eSim Integration**: Wrapper for eSim/ngspice simulation execution
- **Configuration Management**: Flexible configuration system with YAML and environment variable support
- **REST API**: Flask-based API for frontend integration
- **Example Circuits**: Collection of standard circuit designs (Op-Amp, filters, rectifiers)

### Frontend
- **Modern Web UI**: React-based responsive interface
- **Circuit Library**: Browse and view available circuits
- **Circuit Analyzer**: Upload and analyze custom SPICE netlists
- **Simulation Runner**: Execute simulations and view results
- **Tool Manager**: Monitor simulation tools status
- **Configuration Panel**: Manage platform settings

### Deployment
- **Docker Support**: Containerized deployment with docker-compose
- **GCP Ready**: Cloud Run deployment configurations
- **Production Ready**: Optimized builds with nginx and gunicorn

## Project Structure

```
eSIMPlatfornDesignAndArchitecture/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API service layer
│   │   ├── App.jsx              # Main app component
│   │   └── index.js             # Entry point
│   ├── Dockerfile               # Frontend container
│   ├── nginx.conf               # Nginx configuration
│   └── package.json             # Node dependencies
├── backend/                     # Flask REST API
│   ├── api/
│   │   ├── routes/              # API routes
│   │   ├── main.py              # Flask application
│   │   └── utils.py             # Utilities
│   ├── Dockerfile               # Backend container
│   └── requirements-api.txt     # API dependencies
├── src/
│   └── esim_platform/           # Core Python modules
│       ├── circuit_analyzer.py  # Circuit analysis tools
│       ├── esim_wrapper.py      # eSim simulation wrapper
│       └── config_manager.py    # Configuration management
├── circuits/                    # Example circuit designs
│   ├── opamp_noninverting.cir
│   ├── rc_filter.cir
│   ├── voltage_divider.cir
│   └── rectifier.cir
├── gcp/                         # GCP deployment configs
│   ├── cloudbuild.yaml          # Cloud Build configuration
│   ├── backend-service.yaml     # Backend Cloud Run service
│   └── frontend-service.yaml    # Frontend Cloud Run service
├── tests/                       # Unit tests
├── docs/                        # Documentation
├── docker-compose.yml           # Docker Compose configuration
├── DEPLOYMENT.md                # Deployment guide
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Prerequisites

### For Backend Development
- **Python**: 3.9 or higher
- **eSim**: Installed from [esim.fossee.in](https://esim.fossee.in/downloads)
- **ngspice**: Circuit simulator (usually included with eSim)
- **Git**: For version control

### For Frontend Development
- **Node.js**: 18+ and npm
- **Modern web browser**: Chrome, Firefox, Safari, or Edge

### For Docker Deployment
- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher

### For GCP Deployment
- **gcloud CLI**: Latest version
- **GCP Account**: With billing enabled

## Installation

### Quick Start with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture

# Start with Docker Compose
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
```

### Manual Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/findbhavin/eSIMPlatfornDesignAndArchitecture.git
cd eSIMPlatfornDesignAndArchitecture
```

#### 2. Backend Setup

**Set up Python virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Install backend dependencies:**
```bash
pip install -r requirements.txt
pip install -r backend/requirements-api.txt
```

**Configure backend:**
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

**Start backend API:**
```bash
cd backend
python api/main.py
# Backend will run on http://localhost:8000
```

#### 3. Frontend Setup

**Install Node.js dependencies:**
```bash
cd frontend
npm install
```

**Configure frontend:**
```bash
cp .env.example .env
# Edit .env with backend API URL
# REACT_APP_API_URL=http://localhost:8000/api
```

**Start frontend development server:**
```bash
npm start
# Frontend will run on http://localhost:3000
```

### 4. Install eSim (Required for Simulations)

Download and install eSim from the official website:
- **Website**: https://esim.fossee.in/downloads
- **Documentation**: https://esim.fossee.in/resources

Follow the installation instructions for your operating system.

### 5. Verify Installation

**Check backend API:**
```bash
curl http://localhost:8000/api/health
```

**Check if ngspice is available:**
```bash
which ngspice
```

**Run Python tests:**
```bash
pytest tests/
```

## Quick Start

### Using the Web Interface

1. **Start the application:**
   ```bash
   docker-compose up
   ```

2. **Access the web interface:**
   - Open browser to http://localhost:3000
   - Navigate through Dashboard, Circuit Library, Analyzer, etc.

3. **Try the features:**
   - Browse circuits in the Circuit Library
   - Upload and analyze a netlist in Circuit Analyzer
   - Run simulations in Simulation Runner
   - Check tool status in Tool Manager
   - Adjust settings in Configuration Panel

### Using the REST API

**List available circuits:**
```bash
curl http://localhost:8000/api/circuits
```

**Get circuit details:**
```bash
curl http://localhost:8000/api/circuits/voltage_divider
```

**Run simulation:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"circuit_id": "voltage_divider"}'
```

**Check API health:**
```bash
curl http://localhost:8000/api/health
```

### Using Python Modules Directly

**Circuit Analyzer:**
```python
from src.esim_platform import CircuitAnalyzer

# Create analyzer instance
analyzer = CircuitAnalyzer()

# Load and parse a netlist
analyzer.load_netlist('circuits/voltage_divider.cir')
analysis = analyzer.parse_netlist()

print(f"Circuit: {analysis['circuit_name']}")
print(f"Components: {analysis['component_count']}")
print(f"Nodes: {analysis['node_count']}")
```

**eSim Wrapper:**
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

**Configuration Manager:**
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

## Deployment

### Docker Deployment

**Build and run with Docker Compose:**
```bash
# Build and start services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Build individual images:**
```bash
# Backend
docker build -t esim-backend -f backend/Dockerfile .

# Frontend
docker build -t esim-frontend -f frontend/Dockerfile ./frontend
```

### GCP Cloud Run Deployment

For detailed deployment instructions, see **[DEPLOYMENT.md](DEPLOYMENT.md)**.

**Quick deployment:**
```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id

# Deploy using Cloud Build
gcloud builds submit --config=gcp/cloudbuild.yaml .

# Or deploy manually
# 1. Build and push images to Container Registry
# 2. Deploy to Cloud Run
# See DEPLOYMENT.md for complete instructions
```

**Key deployment features:**
- Auto-scaling based on traffic
- HTTPS by default
- Global CDN
- Built-in monitoring and logging
- Cost-effective pay-per-use pricing

## API Documentation

### Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/circuits` | List all circuits |
| GET | `/api/circuits/:id` | Get circuit details |
| POST | `/api/analyze` | Analyze circuit netlist |
| POST | `/api/simulate` | Run circuit simulation |
| GET | `/api/simulation/:id/status` | Get simulation status |
| GET | `/api/config` | Get configuration |
| PUT | `/api/config` | Update configuration |
| GET | `/api/tools` | List tools status |
| POST | `/api/tools/install` | Install tool (placeholder) |

**Example API requests:**

```bash
# Get all circuits
curl http://localhost:8000/api/circuits

# Analyze a circuit file
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@circuits/voltage_divider.cir"

# Run simulation
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{"circuit_id": "voltage_divider"}'
```

## Documentation

Comprehensive documentation is available:

- **[DEPLOYMENT.md](DEPLOYMENT.md)**: Complete deployment guide for Docker and GCP
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

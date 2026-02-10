"""
eSim Wrapper Module

This module provides a wrapper interface for interacting with eSim platform,
including simulation execution and result handling.
"""

import subprocess
import os
from typing import Dict, List, Optional, Tuple


class ESimWrapper:
    """
    Wrapper class for eSim platform operations.
    
    This class provides methods to interact with eSim,
    execute simulations, and process results.
    """
    
    def __init__(self, esim_path: Optional[str] = None):
        """
        Initialize the eSim wrapper.
        
        Args:
            esim_path: Path to eSim installation (optional)
        """
        self.esim_path = esim_path or self._find_esim_path()
        self.simulation_results = {}
        
    def _find_esim_path(self) -> str:
        """
        Attempt to find eSim installation path.
        
        Returns:
            str: Path to eSim or empty string if not found
        """
        # Common eSim installation paths
        common_paths = [
            '/usr/share/esim',
            '/opt/esim',
            os.path.expanduser('~/eSim'),
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return ""
    
    def is_esim_available(self) -> bool:
        """
        Check if eSim is available on the system.
        
        Returns:
            bool: True if eSim is available, False otherwise
        """
        # Check if ngspice (core simulation engine) is available
        try:
            result = subprocess.run(
                ['which', 'ngspice'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def simulate_circuit(self, netlist_path: str) -> Tuple[bool, str]:
        """
        Run eSim simulation on a circuit netlist.
        
        Args:
            netlist_path: Path to the circuit netlist file
            
        Returns:
            Tuple[bool, str]: (success, output/error message)
        """
        if not os.path.exists(netlist_path):
            return False, f"Netlist file not found: {netlist_path}"
        
        try:
            # Run ngspice simulation
            result = subprocess.run(
                ['ngspice', '-b', netlist_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.simulation_results[netlist_path] = result.stdout
                return True, result.stdout
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Simulation timeout (30s exceeded)"
        except FileNotFoundError:
            return False, "ngspice not found. Please install eSim/ngspice."
        except Exception as e:
            return False, f"Simulation error: {str(e)}"
    
    def get_simulation_status(self) -> Dict:
        """
        Get the status of eSim wrapper and capabilities.
        
        Returns:
            Dict: Status information
        """
        return {
            'esim_path': self.esim_path,
            'esim_available': self.is_esim_available(),
            'simulations_run': len(self.simulation_results),
        }
    
    def parse_simulation_output(self, output: str) -> Dict:
        """
        Parse simulation output for key information.
        
        Args:
            output: Simulation output text
            
        Returns:
            Dict: Parsed information
        """
        info = {
            'errors': [],
            'warnings': [],
            'success': False
        }
        
        for line in output.split('\n'):
            line_lower = line.lower()
            if 'error' in line_lower:
                info['errors'].append(line.strip())
            elif 'warning' in line_lower:
                info['warnings'].append(line.strip())
            elif 'simulation completed' in line_lower or 'run completed' in line_lower:
                info['success'] = True
        
        return info
    
    def create_simple_netlist(self, circuit_type: str = "voltage_divider") -> str:
        """
        Create a simple example netlist for testing.
        
        Args:
            circuit_type: Type of circuit to create
            
        Returns:
            str: Netlist content
        """
        netlists = {
            "voltage_divider": """* Simple Voltage Divider Circuit
.title Voltage Divider
V1 1 0 DC 10V
R1 1 2 1k
R2 2 0 1k
.op
.end
""",
            "rc_filter": """* RC Low Pass Filter
.title RC Filter
V1 1 0 AC 1V
R1 1 2 1k
C1 2 0 1u
.ac dec 10 1 1Meg
.end
"""
        }
        
        return netlists.get(circuit_type, netlists["voltage_divider"])

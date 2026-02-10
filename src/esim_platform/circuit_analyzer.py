"""
Circuit Analyzer Module

This module provides functionality to analyze electrical circuits,
including component extraction, node analysis, and parameter calculation.
"""

import re
from typing import Dict, List, Tuple, Optional


class CircuitAnalyzer:
    """
    Analyzes electrical circuits from netlist files.
    
    Attributes:
        netlist_path (str): Path to the circuit netlist file
        components (Dict): Dictionary of circuit components
        nodes (List): List of circuit nodes
    """
    
    def __init__(self, netlist_path: Optional[str] = None):
        """
        Initialize the CircuitAnalyzer.
        
        Args:
            netlist_path: Path to netlist file (optional)
        """
        self.netlist_path = netlist_path
        self.components = {}
        self.nodes = []
        self.circuit_name = ""
        
    def load_netlist(self, path: str) -> bool:
        """
        Load a SPICE netlist file.
        
        Args:
            path: Path to the netlist file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.netlist_path = path
            with open(path, 'r') as f:
                self.netlist_content = f.readlines()
            return True
        except FileNotFoundError:
            print(f"Error: Netlist file not found at {path}")
            return False
        except Exception as e:
            print(f"Error loading netlist: {e}")
            return False
    
    def parse_netlist(self) -> Dict:
        """
        Parse the loaded netlist and extract components.
        
        Returns:
            Dict: Dictionary containing parsed circuit information
        """
        if not hasattr(self, 'netlist_content'):
            return {}
        
        components = []
        nodes = set()
        
        for line in self.netlist_content:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('*') or line.startswith('.'):
                if line.lower().startswith('.title'):
                    self.circuit_name = line.split(None, 1)[1] if len(line.split()) > 1 else ""
                continue
            
            # Parse component line
            parts = line.split()
            if len(parts) >= 3:
                component = {
                    'type': parts[0][0].upper(),
                    'name': parts[0],
                    'nodes': parts[1:3] if len(parts) >= 3 else [],
                    'value': parts[-1] if len(parts) > 3 else None
                }
                components.append(component)
                nodes.update(parts[1:3])
        
        self.components = components
        self.nodes = sorted(list(nodes))
        
        return {
            'circuit_name': self.circuit_name,
            'components': self.components,
            'nodes': self.nodes,
            'component_count': len(self.components),
            'node_count': len(self.nodes)
        }
    
    def get_component_summary(self) -> Dict[str, int]:
        """
        Get a summary of component types in the circuit.
        
        Returns:
            Dict: Count of each component type
        """
        summary = {}
        for comp in self.components:
            comp_type = comp['type']
            summary[comp_type] = summary.get(comp_type, 0) + 1
        return summary
    
    def analyze_circuit(self) -> Dict:
        """
        Perform comprehensive circuit analysis.
        
        Returns:
            Dict: Analysis results including component summary and statistics
        """
        if not self.components:
            return {'error': 'No circuit loaded'}
        
        return {
            'circuit_name': self.circuit_name,
            'total_components': len(self.components),
            'total_nodes': len(self.nodes),
            'component_summary': self.get_component_summary(),
            'nodes': self.nodes,
            'components': self.components
        }
    
    def validate_circuit(self) -> Tuple[bool, List[str]]:
        """
        Validate the circuit for common issues.
        
        Returns:
            Tuple[bool, List[str]]: (is_valid, list of issues)
        """
        issues = []
        
        if not self.components:
            issues.append("Circuit has no components")
        
        if not self.nodes:
            issues.append("Circuit has no nodes")
        
        # Check for ground node
        if '0' not in self.nodes and 'gnd' not in [n.lower() for n in self.nodes]:
            issues.append("Warning: No ground node (0 or GND) found")
        
        return (len(issues) == 0, issues)

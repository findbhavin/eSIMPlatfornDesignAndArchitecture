"""
Unit tests for CircuitAnalyzer module
"""

import pytest
import os
import tempfile
from src.esim_platform.circuit_analyzer import CircuitAnalyzer


class TestCircuitAnalyzer:
    """Test cases for CircuitAnalyzer class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.analyzer = CircuitAnalyzer()
        
        # Create a sample netlist for testing
        self.sample_netlist = """* Sample Circuit
.title Test Circuit
V1 1 0 DC 5V
R1 1 2 1k
R2 2 0 2k
.op
.end
"""
    
    def test_initialization(self):
        """Test CircuitAnalyzer initialization"""
        analyzer = CircuitAnalyzer()
        assert analyzer.netlist_path is None
        assert analyzer.components == {}
        assert analyzer.nodes == []
        
    def test_initialization_with_path(self):
        """Test CircuitAnalyzer initialization with path"""
        analyzer = CircuitAnalyzer("/path/to/netlist.cir")
        assert analyzer.netlist_path == "/path/to/netlist.cir"
    
    def test_load_netlist_success(self):
        """Test loading a valid netlist file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as f:
            f.write(self.sample_netlist)
            temp_path = f.name
        
        try:
            result = self.analyzer.load_netlist(temp_path)
            assert result is True
            assert self.analyzer.netlist_path == temp_path
        finally:
            os.unlink(temp_path)
    
    def test_load_netlist_not_found(self):
        """Test loading a non-existent netlist file"""
        result = self.analyzer.load_netlist("/nonexistent/path.cir")
        assert result is False
    
    def test_parse_netlist(self):
        """Test parsing a netlist"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as f:
            f.write(self.sample_netlist)
            temp_path = f.name
        
        try:
            self.analyzer.load_netlist(temp_path)
            result = self.analyzer.parse_netlist()
            
            assert result['circuit_name'] == 'Test Circuit'
            assert result['component_count'] == 3
            assert len(result['nodes']) > 0
        finally:
            os.unlink(temp_path)
    
    def test_get_component_summary(self):
        """Test getting component summary"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as f:
            f.write(self.sample_netlist)
            temp_path = f.name
        
        try:
            self.analyzer.load_netlist(temp_path)
            self.analyzer.parse_netlist()
            summary = self.analyzer.get_component_summary()
            
            assert 'V' in summary  # Voltage source
            assert 'R' in summary  # Resistors
            assert summary['R'] == 2  # Two resistors
        finally:
            os.unlink(temp_path)
    
    def test_analyze_circuit(self):
        """Test comprehensive circuit analysis"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as f:
            f.write(self.sample_netlist)
            temp_path = f.name
        
        try:
            self.analyzer.load_netlist(temp_path)
            self.analyzer.parse_netlist()
            analysis = self.analyzer.analyze_circuit()
            
            assert 'circuit_name' in analysis
            assert 'total_components' in analysis
            assert 'total_nodes' in analysis
            assert 'component_summary' in analysis
            assert analysis['total_components'] > 0
        finally:
            os.unlink(temp_path)
    
    def test_validate_circuit(self):
        """Test circuit validation"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cir', delete=False) as f:
            f.write(self.sample_netlist)
            temp_path = f.name
        
        try:
            self.analyzer.load_netlist(temp_path)
            self.analyzer.parse_netlist()
            is_valid, issues = self.analyzer.validate_circuit()
            
            assert isinstance(is_valid, bool)
            assert isinstance(issues, list)
        finally:
            os.unlink(temp_path)
    
    def test_empty_circuit_validation(self):
        """Test validation of empty circuit"""
        is_valid, issues = self.analyzer.validate_circuit()
        assert is_valid is False
        assert len(issues) > 0

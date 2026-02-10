"""
Unit tests for ESimWrapper module
"""

import pytest
from src.esim_platform.esim_wrapper import ESimWrapper


class TestESimWrapper:
    """Test cases for ESimWrapper class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.wrapper = ESimWrapper()
    
    def test_initialization(self):
        """Test ESimWrapper initialization"""
        wrapper = ESimWrapper()
        assert wrapper.simulation_results == {}
        assert wrapper.esim_path is not None
    
    def test_initialization_with_path(self):
        """Test ESimWrapper initialization with custom path"""
        custom_path = "/custom/esim/path"
        wrapper = ESimWrapper(custom_path)
        assert wrapper.esim_path == custom_path
    
    def test_is_esim_available(self):
        """Test checking if eSim is available"""
        result = self.wrapper.is_esim_available()
        assert isinstance(result, bool)
    
    def test_get_simulation_status(self):
        """Test getting simulation status"""
        status = self.wrapper.get_simulation_status()
        
        assert 'esim_path' in status
        assert 'esim_available' in status
        assert 'simulations_run' in status
        assert isinstance(status['esim_available'], bool)
        assert status['simulations_run'] == 0
    
    def test_parse_simulation_output_with_errors(self):
        """Test parsing simulation output with errors"""
        output = """Error: Cannot find file
Warning: Temperature not specified
Some other output"""
        
        info = self.wrapper.parse_simulation_output(output)
        
        assert 'errors' in info
        assert 'warnings' in info
        assert len(info['errors']) == 1
        assert len(info['warnings']) == 1
    
    def test_parse_simulation_output_success(self):
        """Test parsing successful simulation output"""
        output = """Starting simulation...
Simulation completed successfully
Output generated"""
        
        info = self.wrapper.parse_simulation_output(output)
        assert info['success'] is True
    
    def test_create_simple_netlist_voltage_divider(self):
        """Test creating voltage divider netlist"""
        netlist = self.wrapper.create_simple_netlist("voltage_divider")
        assert "Voltage Divider" in netlist
        assert "V1" in netlist
        assert "R1" in netlist
        assert ".end" in netlist
    
    def test_create_simple_netlist_rc_filter(self):
        """Test creating RC filter netlist"""
        netlist = self.wrapper.create_simple_netlist("rc_filter")
        assert "RC Filter" in netlist or "RC" in netlist
        assert "C1" in netlist
        assert ".end" in netlist
    
    def test_create_simple_netlist_default(self):
        """Test creating netlist with invalid type returns default"""
        netlist = self.wrapper.create_simple_netlist("invalid_type")
        assert "Voltage Divider" in netlist  # Should return default
    
    def test_simulate_circuit_file_not_found(self):
        """Test simulating with non-existent file"""
        success, message = self.wrapper.simulate_circuit("/nonexistent/file.cir")
        assert success is False
        assert "not found" in message.lower()

"""
Unit tests for ConfigManager module
"""

import pytest
import os
import tempfile
import yaml
from src.esim_platform.config_manager import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.config_manager = ConfigManager()
    
    def test_initialization(self):
        """Test ConfigManager initialization"""
        manager = ConfigManager()
        assert manager.config is not None
        assert 'esim' in manager.config
        assert 'simulation' in manager.config
        assert 'circuit' in manager.config
    
    def test_default_config_values(self):
        """Test default configuration values"""
        assert self.config_manager.get('esim.timeout') == 30
        assert self.config_manager.get('simulation.verbosity') == 'normal'
        assert self.config_manager.get('circuit.default_ground') == '0'
    
    def test_get_with_default(self):
        """Test getting config value with default"""
        value = self.config_manager.get('nonexistent.key', 'default_value')
        assert value == 'default_value'
    
    def test_set_and_get(self):
        """Test setting and getting config values"""
        self.config_manager.set('esim.timeout', 60)
        assert self.config_manager.get('esim.timeout') == 60
    
    def test_set_nested_key(self):
        """Test setting nested configuration key"""
        self.config_manager.set('new.nested.key', 'value')
        assert self.config_manager.get('new.nested.key') == 'value'
    
    def test_get_all(self):
        """Test getting all configuration"""
        config = self.config_manager.get_all()
        assert isinstance(config, dict)
        assert 'esim' in config
        assert 'simulation' in config
    
    def test_load_from_file(self):
        """Test loading configuration from YAML file"""
        test_config = {
            'esim': {
                'timeout': 45,
                'custom_key': 'custom_value'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            temp_path = f.name
        
        try:
            result = self.config_manager.load_from_file(temp_path)
            assert result is True
            assert self.config_manager.get('esim.timeout') == 45
            assert self.config_manager.get('esim.custom_key') == 'custom_value'
        finally:
            os.unlink(temp_path)
    
    def test_load_from_file_not_found(self):
        """Test loading from non-existent file"""
        result = self.config_manager.load_from_file('/nonexistent/config.yaml')
        assert result is False
    
    def test_save_to_file(self):
        """Test saving configuration to file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            self.config_manager.set('test.key', 'test_value')
            result = self.config_manager.save_to_file(temp_path)
            assert result is True
            
            # Verify the file was created and contains the data
            with open(temp_path, 'r') as f:
                saved_config = yaml.safe_load(f)
            assert 'test' in saved_config
            assert saved_config['test']['key'] == 'test_value'
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_load_from_env(self):
        """Test loading configuration from environment variables"""
        os.environ['ESIM_INSTALLATION_PATH'] = '/custom/esim/path'
        os.environ['ESIM_TIMEOUT'] = '90'
        
        manager = ConfigManager()
        
        assert manager.get('esim.installation_path') == '/custom/esim/path'
        assert manager.get('esim.timeout') == 90
        
        # Clean up
        del os.environ['ESIM_INSTALLATION_PATH']
        del os.environ['ESIM_TIMEOUT']
    
    def test_initialization_with_config_file(self):
        """Test initialization with config file"""
        test_config = {'esim': {'timeout': 120}}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_config, f)
            temp_path = f.name
        
        try:
            manager = ConfigManager(temp_path)
            assert manager.get('esim.timeout') == 120
        finally:
            os.unlink(temp_path)

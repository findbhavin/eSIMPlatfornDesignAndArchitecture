"""
Configuration Manager Module

This module handles configuration management for the eSim platform integration,
including loading settings from files and environment variables.
"""

import os
import yaml
from typing import Dict, Any, Optional


class ConfigManager:
    """
    Manages configuration for eSim platform integration.
    
    Supports loading configuration from YAML files and environment variables.
    """
    
    DEFAULT_CONFIG = {
        'esim': {
            'installation_path': '/usr/share/esim',
            'ngspice_path': '/usr/bin/ngspice',
            'timeout': 30,
        },
        'simulation': {
            'output_dir': './simulation_results',
            'keep_intermediate_files': False,
            'verbosity': 'normal',
        },
        'circuit': {
            'default_ground': '0',
            'default_temp': 27,
            'default_precision': 1e-6,
        }
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to YAML configuration file (optional)
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_file = config_file
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        
        self.load_from_env()
    
    def load_from_file(self, filepath: str) -> bool:
        """
        Load configuration from a YAML file.
        
        Args:
            filepath: Path to the YAML configuration file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_config(file_config)
            return True
        except Exception as e:
            print(f"Error loading config file: {e}")
            return False
    
    def load_from_env(self):
        """
        Load configuration from environment variables.
        
        Environment variables should be prefixed with ESIM_
        Example: ESIM_INSTALLATION_PATH, ESIM_TIMEOUT
        """
        # eSim installation path
        if 'ESIM_INSTALLATION_PATH' in os.environ:
            self.config['esim']['installation_path'] = os.environ['ESIM_INSTALLATION_PATH']
        
        # Simulation timeout
        if 'ESIM_TIMEOUT' in os.environ:
            try:
                self.config['esim']['timeout'] = int(os.environ['ESIM_TIMEOUT'])
            except ValueError:
                pass
        
        # Output directory
        if 'ESIM_OUTPUT_DIR' in os.environ:
            self.config['simulation']['output_dir'] = os.environ['ESIM_OUTPUT_DIR']
    
    def _merge_config(self, new_config: Dict):
        """
        Merge new configuration with existing configuration.
        
        Args:
            new_config: New configuration dictionary to merge
        """
        for key, value in new_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Configuration key path (e.g., 'esim.timeout')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Configuration key path (e.g., 'esim.timeout')
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_all(self) -> Dict:
        """
        Get the entire configuration dictionary.
        
        Returns:
            Dict: Complete configuration
        """
        return self.config.copy()
    
    def save_to_file(self, filepath: str) -> bool:
        """
        Save current configuration to a YAML file.
        
        Args:
            filepath: Path where to save the configuration
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error saving config file: {e}")
            return False

"""
Configuration Handling Module

This module manages configuration settings for eSim-related tools including environment
variables, PATH configuration, and tool-specific settings.

Author: eSim Tool Manager Team
License: MIT
"""

import os
import sys
import json
import yaml
import logging
import shutil
from typing import Dict, Optional, Any, List
from pathlib import Path
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration for eSim-related tools.
    
    Attributes:
        config_file (Path): Path to the configuration file
        config (Dict): Current configuration dictionary
        backup_dir (Path): Directory for configuration backups
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the ConfigManager.
        
        Args:
            config_file (Optional[str]): Path to config file (default: tool_manager/config.yaml)
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            config_dir = Path(__file__).parent
            self.config_file = config_dir / 'config.yaml'
        
        # Setup backup directory
        self.backup_dir = Path(__file__).parent / 'config_backups'
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load or create default configuration
        self.config = self._load_config()
        logger.info(f"ConfigManager initialized with config file: {self.config_file}")
    
    def _load_config(self) -> Dict:
        """
        Load configuration from file or create default.
        
        Returns:
            Dict: Configuration dictionary
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    if self.config_file.suffix == '.yaml' or self.config_file.suffix == '.yml':
                        config = yaml.safe_load(f)
                    else:
                        config = json.load(f)
                logger.info("Configuration loaded successfully")
                return config or {}
            except Exception as e:
                logger.error(f"Error loading configuration: {e}")
                return self._get_default_config()
        else:
            logger.info("No configuration file found, creating default")
            config = self._get_default_config()
            self._save_config(config)
            return config
    
    def _get_default_config(self) -> Dict:
        """
        Get default configuration.
        
        Returns:
            Dict: Default configuration dictionary
        """
        os_type = platform.system().lower()
        
        default_config = {
            'system': {
                'os': os_type,
                'python_version': f"{sys.version_info.major}.{sys.version_info.minor}"
            },
            'tools': {
                'ngspice': {
                    'enabled': True,
                    'auto_update': False,
                    'path': '',
                    'environment_vars': {
                        'SPICE_LIB_DIR': '',
                        'SPICE_EXEC_DIR': ''
                    }
                },
                'kicad': {
                    'enabled': True,
                    'auto_update': False,
                    'path': '',
                    'environment_vars': {
                        'KICAD_SYMBOL_DIR': '',
                        'KICAD_FOOTPRINT_DIR': ''
                    }
                }
            },
            'paths': {
                'install_dir': str(Path.home() / '.esim_tools'),
                'cache_dir': str(Path.home() / '.esim_tools' / 'cache'),
                'log_dir': str(Path.home() / '.esim_tools' / 'logs')
            },
            'update': {
                'check_on_startup': True,
                'auto_install': False,
                'update_interval_days': 7
            },
            'logging': {
                'level': 'INFO',
                'file_logging': True,
                'console_logging': True
            }
        }
        
        return default_config
    
    def _save_config(self, config: Optional[Dict] = None):
        """
        Save configuration to file.
        
        Args:
            config (Optional[Dict]): Configuration to save (uses self.config if None)
        """
        config = config or self.config
        
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                if self.config_file.suffix == '.yaml' or self.config_file.suffix == '.yml':
                    yaml.dump(config, f, default_flow_style=False, indent=2)
                else:
                    json.dump(config, f, indent=2)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'tools.ngspice.enabled')
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value or default
            
        Example:
            >>> config = ConfigManager()
            >>> enabled = config.get('tools.ngspice.enabled', True)
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'tools.ngspice.enabled')
            value (Any): Value to set
            
        Example:
            >>> config = ConfigManager()
            >>> config.set('tools.ngspice.enabled', False)
            >>> config.save()
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        logger.debug(f"Set configuration: {key} = {value}")
    
    def save(self):
        """Save current configuration to file."""
        self._save_config()
    
    def backup_config(self) -> bool:
        """
        Create a backup of the current configuration.
        
        Returns:
            bool: True if backup succeeded, False otherwise
        """
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f"config_backup_{timestamp}.yaml"
            
            shutil.copy2(self.config_file, backup_file)
            logger.info(f"Configuration backed up to {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Error backing up configuration: {e}")
            return False
    
    def restore_config(self, backup_file: str) -> bool:
        """
        Restore configuration from a backup file.
        
        Args:
            backup_file (str): Path to backup file
            
        Returns:
            bool: True if restore succeeded, False otherwise
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_file}")
                return False
            
            shutil.copy2(backup_path, self.config_file)
            self.config = self._load_config()
            logger.info(f"Configuration restored from {backup_file}")
            return True
        except Exception as e:
            logger.error(f"Error restoring configuration: {e}")
            return False
    
    def configure_tool(self, tool_name: str, config_settings: Dict) -> bool:
        """
        Configure a specific tool with custom settings.
        
        Args:
            tool_name (str): Name of the tool (e.g., 'ngspice', 'kicad')
            config_settings (Dict): Configuration settings for the tool
            
        Returns:
            bool: True if configuration succeeded, False otherwise
            
        Example:
            >>> config = ConfigManager()
            >>> settings = {'enabled': True, 'auto_update': True}
            >>> config.configure_tool('ngspice', settings)
        """
        tool_name_lower = tool_name.lower()
        
        try:
            # Update tool configuration
            if 'tools' not in self.config:
                self.config['tools'] = {}
            
            if tool_name_lower not in self.config['tools']:
                self.config['tools'][tool_name_lower] = {}
            
            # Merge settings
            self.config['tools'][tool_name_lower].update(config_settings)
            
            # Apply environment variables if specified
            if 'environment_vars' in config_settings:
                for var_name, var_value in config_settings['environment_vars'].items():
                    if var_value:
                        self.set_env_var(var_name, var_value)
            
            # Apply PATH if specified
            if 'path' in config_settings and config_settings['path']:
                self.add_to_path(config_settings['path'])
            
            self._save_config()
            logger.info(f"Configuration applied for {tool_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error configuring {tool_name}: {e}")
            return False
    
    def set_env_var(self, var_name: str, value: str, persistent: bool = False):
        """
        Set an environment variable.
        
        Args:
            var_name (str): Name of the environment variable
            value (str): Value to set
            persistent (bool): Whether to persist across sessions (requires shell config)
            
        Example:
            >>> config = ConfigManager()
            >>> config.set_env_var('SPICE_LIB_DIR', '/usr/local/share/ngspice')
        """
        os.environ[var_name] = value
        logger.info(f"Set environment variable: {var_name}={value}")
        
        if persistent:
            self._persist_env_var(var_name, value)
    
    def _persist_env_var(self, var_name: str, value: str):
        """
        Persist environment variable to shell configuration.
        
        Args:
            var_name (str): Variable name
            value (str): Variable value
            
        Note:
            This is a simplified implementation. In production, you would
            need to handle different shells and platforms appropriately.
        """
        os_type = platform.system().lower()
        
        if os_type == 'linux' or os_type == 'darwin':
            # Try to add to .bashrc or .zshrc
            shell_configs = [
                Path.home() / '.bashrc',
                Path.home() / '.zshrc',
                Path.home() / '.profile'
            ]
            
            export_line = f'export {var_name}="{value}"\n'
            
            for config_file in shell_configs:
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            content = f.read()
                        
                        # Check if variable already exists
                        if f'export {var_name}=' not in content:
                            with open(config_file, 'a') as f:
                                f.write(f'\n# Added by eSim Tool Manager\n')
                                f.write(export_line)
                            logger.info(f"Added {var_name} to {config_file}")
                        else:
                            logger.info(f"{var_name} already exists in {config_file}")
                        break
                    except Exception as e:
                        logger.error(f"Error updating {config_file}: {e}")
        
        elif os_type == 'windows':
            # On Windows, would use setx command
            logger.info(f"For persistent environment variables on Windows, use: setx {var_name} \"{value}\"")
    
    def add_to_path(self, path: str, persistent: bool = False):
        """
        Add a directory to the system PATH.
        
        Args:
            path (str): Directory path to add
            persistent (bool): Whether to persist across sessions
            
        Example:
            >>> config = ConfigManager()
            >>> config.add_to_path('/usr/local/bin/ngspice')
        """
        path = str(Path(path).resolve())
        
        # Add to current session
        current_path = os.environ.get('PATH', '')
        if path not in current_path:
            os.environ['PATH'] = f"{path}{os.pathsep}{current_path}"
            logger.info(f"Added to PATH: {path}")
        else:
            logger.info(f"Path already in PATH: {path}")
        
        if persistent:
            self._persist_path(path)
    
    def _persist_path(self, path: str):
        """
        Persist PATH addition to shell configuration.
        
        Args:
            path (str): Path to persist
        """
        os_type = platform.system().lower()
        
        if os_type == 'linux' or os_type == 'darwin':
            shell_configs = [
                Path.home() / '.bashrc',
                Path.home() / '.zshrc',
                Path.home() / '.profile'
            ]
            
            path_line = f'export PATH="{path}:$PATH"\n'
            
            for config_file in shell_configs:
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            content = f.read()
                        
                        if path not in content:
                            with open(config_file, 'a') as f:
                                f.write(f'\n# Added by eSim Tool Manager\n')
                                f.write(path_line)
                            logger.info(f"Added path to {config_file}")
                        else:
                            logger.info(f"Path already exists in {config_file}")
                        break
                    except Exception as e:
                        logger.error(f"Error updating {config_file}: {e}")
        
        elif os_type == 'windows':
            logger.info(f"For persistent PATH on Windows, manually add to system environment variables")
    
    def validate_config(self) -> List[str]:
        """
        Validate the current configuration and return any issues.
        
        Returns:
            List[str]: List of validation issues (empty if valid)
        """
        issues = []
        
        # Check required keys
        required_keys = ['system', 'tools', 'paths']
        for key in required_keys:
            if key not in self.config:
                issues.append(f"Missing required configuration section: {key}")
        
        # Validate paths exist
        if 'paths' in self.config:
            for path_key, path_value in self.config['paths'].items():
                if path_value:
                    path = Path(path_value)
                    if not path.exists() and path_key != 'install_dir':
                        issues.append(f"Path does not exist: {path_key} = {path_value}")
        
        # Validate tool configurations
        if 'tools' in self.config:
            for tool_name, tool_config in self.config['tools'].items():
                if not isinstance(tool_config, dict):
                    issues.append(f"Invalid tool configuration for {tool_name}")
        
        if issues:
            logger.warning(f"Configuration validation found {len(issues)} issue(s)")
        else:
            logger.info("Configuration validation passed")
        
        return issues
    
    def reset_to_default(self):
        """Reset configuration to default values."""
        self.config = self._get_default_config()
        self._save_config()
        logger.info("Configuration reset to default")


def configure_tool(tool_name: str, config_settings: Dict) -> bool:
    """
    Convenience function to configure a tool.
    
    Args:
        tool_name (str): Name of the tool
        config_settings (Dict): Configuration settings
        
    Returns:
        bool: True if successful, False otherwise
    """
    config_manager = ConfigManager()
    return config_manager.configure_tool(tool_name, config_settings)


def set_env_var(var_name: str, value: str, persistent: bool = False):
    """
    Convenience function to set an environment variable.
    
    Args:
        var_name (str): Variable name
        value (str): Variable value
        persistent (bool): Whether to persist
    """
    config_manager = ConfigManager()
    config_manager.set_env_var(var_name, value, persistent)


if __name__ == "__main__":
    # Demo usage
    config = ConfigManager()
    
    print(f"Configuration file: {config.config_file}")
    print(f"\nCurrent OS: {config.get('system.os')}")
    print(f"Python version: {config.get('system.python_version')}")
    
    print("\nTool configurations:")
    for tool in ['ngspice', 'kicad']:
        enabled = config.get(f'tools.{tool}.enabled', False)
        print(f"  {tool}: {'Enabled' if enabled else 'Disabled'}")
    
    print("\nValidating configuration...")
    issues = config.validate_config()
    if issues:
        print("Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Configuration is valid")

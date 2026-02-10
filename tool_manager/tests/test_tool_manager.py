"""
Unit Tests for eSim Tool Manager

Basic unit tests for the tool manager modules.

Author: eSim Tool Manager Team
License: MIT
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from installation import ToolInstaller, get_installed_tools
from update import ToolUpdater
from config import ConfigManager
from dependency import DependencyChecker


class TestToolInstaller(unittest.TestCase):
    """Test cases for ToolInstaller class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.installer = ToolInstaller()
    
    def test_os_detection(self):
        """Test that OS is detected correctly."""
        self.assertIn(self.installer.os_type, ['linux', 'windows', 'darwin'])
    
    def test_get_installed_tools(self):
        """Test getting installed tools."""
        tools = self.installer.get_installed_tools()
        self.assertIsInstance(tools, dict)
    
    def test_is_tool_installed(self):
        """Test checking if a tool is installed."""
        # Test with a common tool that should exist
        result = self.installer.is_tool_installed('python')
        # Result can be True or False depending on system
        self.assertIsInstance(result, bool)
    
    def test_verify_installation(self):
        """Test installation verification."""
        # This will return False for non-existent tools
        result = self.installer.verify_installation('nonexistent_tool_xyz')
        self.assertFalse(result)


class TestToolUpdater(unittest.TestCase):
    """Test cases for ToolUpdater class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use temporary log file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, 'test_updates.json')
        self.updater = ToolUpdater(log_file=self.log_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        os.rmdir(self.temp_dir)
    
    def test_log_action(self):
        """Test logging an action."""
        self.updater.log_action('test', 'success', 'test_tool', 'Test details')
        
        # Check that log was created
        self.assertTrue(os.path.exists(self.log_file))
        
        # Check log contents
        with open(self.log_file, 'r') as f:
            logs = json.load(f)
        
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['action'], 'test')
        self.assertEqual(logs[0]['status'], 'success')
        self.assertEqual(logs[0]['tool_name'], 'test_tool')
    
    def test_get_update_history(self):
        """Test getting update history."""
        # Add some test logs
        self.updater.log_action('update', 'success', 'tool1', 'Updated')
        self.updater.log_action('update', 'success', 'tool2', 'Updated')
        
        history = self.updater.get_update_history()
        self.assertEqual(len(history), 2)
        
        # Test filtering by tool
        history_filtered = self.updater.get_update_history(tool_name='tool1')
        self.assertEqual(len(history_filtered), 1)
        self.assertEqual(history_filtered[0]['tool_name'], 'tool1')
    
    def test_get_latest_version_info(self):
        """Test getting latest version information."""
        info = self.updater.get_latest_version_info('ngspice')
        
        if info:
            self.assertIsInstance(info, dict)
            self.assertIn('latest_version', info)


class TestConfigManager(unittest.TestCase):
    """Test cases for ConfigManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Use temporary config file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.yaml')
        self.config_mgr = ConfigManager(config_file=self.config_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        
        # Clean up backup directory
        backup_dir = Path(self.config_file).parent / 'config_backups'
        if backup_dir.exists():
            for backup_file in backup_dir.iterdir():
                backup_file.unlink()
            backup_dir.rmdir()
        
        os.rmdir(self.temp_dir)
    
    def test_config_creation(self):
        """Test that default config is created."""
        self.assertTrue(os.path.exists(self.config_file))
    
    def test_get_config_value(self):
        """Test getting configuration values."""
        # Test existing key
        os_type = self.config_mgr.get('system.os')
        self.assertIsNotNone(os_type)
        
        # Test non-existing key with default
        value = self.config_mgr.get('non.existing.key', 'default')
        self.assertEqual(value, 'default')
    
    def test_set_config_value(self):
        """Test setting configuration values."""
        self.config_mgr.set('test.key', 'test_value')
        value = self.config_mgr.get('test.key')
        self.assertEqual(value, 'test_value')
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Set a test value
        self.config_mgr.set('test.setting', 'test123')
        self.config_mgr.save()
        
        # Create new config manager with same file
        new_config_mgr = ConfigManager(config_file=self.config_file)
        value = new_config_mgr.get('test.setting')
        self.assertEqual(value, 'test123')
    
    def test_configure_tool(self):
        """Test configuring a tool."""
        settings = {
            'enabled': True,
            'auto_update': False,
            'path': '/test/path'
        }
        
        success = self.config_mgr.configure_tool('test_tool', settings)
        self.assertTrue(success)
        
        # Verify settings were applied
        self.assertTrue(self.config_mgr.get('tools.test_tool.enabled'))
        self.assertFalse(self.config_mgr.get('tools.test_tool.auto_update'))
    
    def test_validate_config(self):
        """Test configuration validation."""
        issues = self.config_mgr.validate_config()
        # Should be a list (empty or with issues)
        self.assertIsInstance(issues, list)


class TestDependencyChecker(unittest.TestCase):
    """Test cases for DependencyChecker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.checker = DependencyChecker()
    
    def test_os_detection(self):
        """Test OS detection."""
        self.assertIn(self.checker.os_type, ['linux', 'windows', 'darwin'])
    
    def test_check_python_version(self):
        """Test Python version checking."""
        # Should pass for current Python version
        result = self.checker.check_python_version((3, 6))
        self.assertTrue(result)
        
        # Should fail for impossibly high version
        result = self.checker.check_python_version((99, 0))
        self.assertFalse(result)
    
    def test_check_python_package(self):
        """Test Python package checking."""
        # sys should always be available
        result = self.checker.check_python_package('sys')
        self.assertTrue(result)
        
        # Non-existent package should return False
        result = self.checker.check_python_package('nonexistent_package_xyz123')
        self.assertFalse(result)
    
    def test_check_dependencies(self):
        """Test checking dependencies for a tool."""
        issues = self.checker.check_dependencies('python')
        # Should return a list
        self.assertIsInstance(issues, list)
    
    def test_check_all_tools(self):
        """Test checking all tools."""
        all_issues = self.checker.check_all_tools()
        
        # Should return a dict
        self.assertIsInstance(all_issues, dict)
        
        # Should include expected tools
        self.assertIn('python', all_issues)
        self.assertIn('ngspice', all_issues)
        self.assertIn('kicad', all_issues)
    
    def test_get_system_info(self):
        """Test getting system information."""
        sys_info = self.checker.get_system_info()
        
        self.assertIsInstance(sys_info, dict)
        self.assertIn('os', sys_info)
        self.assertIn('python_version', sys_info)
        self.assertIn('platform', sys_info)


class TestIntegration(unittest.TestCase):
    """Integration tests for tool manager."""
    
    def test_installer_and_checker_integration(self):
        """Test integration between installer and dependency checker."""
        installer = ToolInstaller()
        checker = DependencyChecker()
        
        # Get installed tools
        tools = installer.get_installed_tools()
        
        # Check dependencies for each installed tool
        for tool in tools:
            issues = checker.check_dependencies(tool)
            # Should return a list (possibly empty)
            self.assertIsInstance(issues, list)
    
    def test_config_and_installer_integration(self):
        """Test integration between config and installer."""
        temp_dir = tempfile.mkdtemp()
        config_file = os.path.join(temp_dir, 'test_config.yaml')
        
        try:
            config_mgr = ConfigManager(config_file=config_file)
            installer = ToolInstaller()
            
            # Configure a tool setting
            config_mgr.set('tools.ngspice.enabled', True)
            
            # Check if config is accessible
            enabled = config_mgr.get('tools.ngspice.enabled')
            self.assertTrue(enabled)
            
        finally:
            if os.path.exists(config_file):
                os.remove(config_file)
            os.rmdir(temp_dir)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestToolInstaller))
    suite.addTests(loader.loadTestsFromTestCase(TestToolUpdater))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigManager))
    suite.addTests(loader.loadTestsFromTestCase(TestDependencyChecker))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())

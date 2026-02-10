"""
Dependency Checker Module

This module checks, validates, and reports on dependencies required for eSim-related tools.

Author: eSim Tool Manager Team
License: MIT
"""

import sys
import os
import platform
import subprocess
import logging
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import importlib.util

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DependencyChecker:
    """
    Checks and validates dependencies for eSim-related tools.
    
    Attributes:
        os_type (str): Detected operating system
        python_version (Tuple): Python version tuple
        issues (List[str]): List of dependency issues found
    """
    
    def __init__(self):
        """Initialize the DependencyChecker."""
        self.os_type = platform.system().lower()
        self.python_version = sys.version_info
        self.issues: List[str] = []
        logger.info(f"DependencyChecker initialized for {self.os_type}")
    
    def check_python_version(self, min_version: Tuple[int, int] = (3, 7)) -> bool:
        """
        Check if Python version meets minimum requirements.
        
        Args:
            min_version (Tuple[int, int]): Minimum required version (major, minor)
            
        Returns:
            bool: True if version is sufficient, False otherwise
        """
        current = (self.python_version.major, self.python_version.minor)
        required = min_version
        
        if current >= required:
            logger.info(f"Python version {current[0]}.{current[1]} meets requirements (>= {required[0]}.{required[1]})")
            return True
        else:
            issue = f"Python version {current[0]}.{current[1]} is below minimum {required[0]}.{required[1]}"
            logger.error(issue)
            self.issues.append(issue)
            return False
    
    def check_python_package(self, package_name: str, min_version: Optional[str] = None) -> bool:
        """
        Check if a Python package is installed.
        
        Args:
            package_name (str): Name of the package
            min_version (Optional[str]): Minimum required version
            
        Returns:
            bool: True if package is available, False otherwise
        """
        try:
            spec = importlib.util.find_spec(package_name)
            if spec is None:
                issue = f"Python package '{package_name}' is not installed"
                logger.warning(issue)
                self.issues.append(issue)
                return False
            
            # Try to get version
            if min_version:
                try:
                    module = importlib.import_module(package_name)
                    if hasattr(module, '__version__'):
                        from packaging import version
                        installed_version = module.__version__
                        if version.parse(installed_version) >= version.parse(min_version):
                            logger.info(f"Package '{package_name}' version {installed_version} meets requirements")
                            return True
                        else:
                            issue = f"Package '{package_name}' version {installed_version} is below minimum {min_version}"
                            logger.warning(issue)
                            self.issues.append(issue)
                            return False
                except Exception as e:
                    logger.debug(f"Could not verify version for {package_name}: {e}")
            
            logger.info(f"Python package '{package_name}' is installed")
            return True
            
        except Exception as e:
            issue = f"Error checking package '{package_name}': {e}"
            logger.error(issue)
            self.issues.append(issue)
            return False
    
    def check_system_command(self, command: str, expected_in_output: Optional[str] = None) -> bool:
        """
        Check if a system command is available.
        
        Args:
            command (str): Command to check
            expected_in_output (Optional[str]): Expected string in command output
            
        Returns:
            bool: True if command is available, False otherwise
        """
        try:
            # Check using 'which' or 'where'
            check_cmd = 'where' if self.os_type == 'windows' else 'which'
            result = subprocess.run(
                [check_cmd, command],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info(f"System command '{command}' is available")
                return True
            else:
                issue = f"System command '{command}' is not available"
                logger.warning(issue)
                self.issues.append(issue)
                return False
                
        except Exception as e:
            issue = f"Error checking command '{command}': {e}"
            logger.error(issue)
            self.issues.append(issue)
            return False
    
    def check_system_library(self, library_name: str) -> bool:
        """
        Check if a system library is installed.
        
        Args:
            library_name (str): Name of the library
            
        Returns:
            bool: True if library is found, False otherwise
            
        Note:
            This is a basic check that works differently per platform
        """
        if self.os_type == 'linux':
            # Check common library locations
            lib_paths = [
                '/usr/lib',
                '/usr/local/lib',
                '/lib',
                '/usr/lib/x86_64-linux-gnu',
                '/usr/lib64'
            ]
            
            for lib_path in lib_paths:
                lib_dir = Path(lib_path)
                if lib_dir.exists():
                    # Look for library files
                    lib_files = list(lib_dir.glob(f"{library_name}*"))
                    if lib_files:
                        logger.info(f"System library '{library_name}' found at {lib_path}")
                        return True
            
            issue = f"System library '{library_name}' not found"
            logger.warning(issue)
            self.issues.append(issue)
            return False
            
        elif self.os_type == 'darwin':
            # macOS library check
            lib_paths = ['/usr/lib', '/usr/local/lib', '/opt/homebrew/lib']
            for lib_path in lib_paths:
                lib_dir = Path(lib_path)
                if lib_dir.exists():
                    lib_files = list(lib_dir.glob(f"{library_name}*"))
                    if lib_files:
                        logger.info(f"System library '{library_name}' found")
                        return True
            
            issue = f"System library '{library_name}' not found"
            logger.warning(issue)
            self.issues.append(issue)
            return False
            
        else:
            # Windows - would need to check registry or specific paths
            logger.info(f"Library check not fully implemented for {self.os_type}")
            return True
    
    def check_dependencies(self, tool_name: str) -> List[str]:
        """
        Check all dependencies for a specific tool.
        
        Args:
            tool_name (str): Name of the tool ('ngspice', 'kicad', or 'python')
            
        Returns:
            List[str]: List of missing or incompatible dependencies
            
        Example:
            >>> checker = DependencyChecker()
            >>> issues = checker.check_dependencies('ngspice')
            >>> if issues:
            ...     print("Missing dependencies:", issues)
        """
        self.issues = []
        tool_name_lower = tool_name.lower()
        
        logger.info(f"Checking dependencies for {tool_name}")
        
        if tool_name_lower == 'python':
            self._check_python_dependencies()
        elif tool_name_lower == 'ngspice':
            self._check_ngspice_dependencies()
        elif tool_name_lower == 'kicad':
            self._check_kicad_dependencies()
        else:
            logger.warning(f"Unknown tool: {tool_name}")
            self.issues.append(f"Unknown tool: {tool_name}")
        
        return self.issues
    
    def _check_python_dependencies(self):
        """Check Python environment dependencies."""
        # Check Python version
        self.check_python_version((3, 7))
        
        # Check required Python packages
        required_packages = {
            'requests': '2.28.0',
            'click': '8.1.0',
            'colorama': '0.4.6',
            'pyyaml': '6.0',
            'packaging': '21.0'
        }
        
        for package, min_ver in required_packages.items():
            self.check_python_package(package, min_ver)
    
    def _check_ngspice_dependencies(self):
        """Check dependencies for ngspice."""
        # Check if ngspice command is available
        self.check_system_command('ngspice')
        
        # Check for common ngspice dependencies on Linux
        if self.os_type == 'linux':
            # These are typical dependencies, may vary by distribution
            deps = ['libx11', 'libxaw', 'libreadline']
            for dep in deps:
                self.check_system_library(dep)
        
        # Check environment variables
        if not os.environ.get('SPICE_LIB_DIR'):
            logger.info("SPICE_LIB_DIR environment variable not set (optional)")
    
    def _check_kicad_dependencies(self):
        """Check dependencies for KiCad."""
        # Check if kicad command is available
        kicad_commands = ['kicad', 'kicad-cli']
        found = False
        
        for cmd in kicad_commands:
            if self.check_system_command(cmd):
                found = True
                break
        
        if not found:
            issue = "KiCad not found (neither 'kicad' nor 'kicad-cli' command available)"
            logger.warning(issue)
            self.issues.append(issue)
        
        # Check for Python bindings (optional)
        if self.check_python_package('pcbnew'):
            logger.info("KiCad Python bindings (pcbnew) available")
        else:
            logger.info("KiCad Python bindings not available (optional)")
    
    def check_all_tools(self) -> Dict[str, List[str]]:
        """
        Check dependencies for all supported tools.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping tool names to their dependency issues
            
        Example:
            >>> checker = DependencyChecker()
            >>> all_issues = checker.check_all_tools()
            >>> for tool, issues in all_issues.items():
            ...     if issues:
            ...         print(f"{tool}: {len(issues)} issues found")
        """
        tools = ['python', 'ngspice', 'kicad']
        all_issues = {}
        
        for tool in tools:
            issues = self.check_dependencies(tool)
            all_issues[tool] = issues
        
        return all_issues
    
    def report_dependency_issues(self, issues: List[str]):
        """
        Report dependency issues in a formatted manner.
        
        Args:
            issues (List[str]): List of dependency issues to report
            
        Example:
            >>> checker = DependencyChecker()
            >>> issues = checker.check_dependencies('ngspice')
            >>> checker.report_dependency_issues(issues)
        """
        if not issues:
            print("\n✓ All dependencies are satisfied")
            logger.info("All dependencies satisfied")
            return
        
        print(f"\n⚠ Found {len(issues)} dependency issue(s):")
        print("=" * 60)
        
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        print("=" * 60)
        print("\nRecommended actions:")
        
        # Provide context-specific recommendations
        if any('Python version' in issue for issue in issues):
            print("  - Upgrade Python to version 3.7 or higher")
        
        if any('package' in issue.lower() for issue in issues):
            print("  - Install missing Python packages:")
            print("    pip install -r requirements.txt")
        
        if any('ngspice' in issue.lower() for issue in issues):
            print("  - Install ngspice:")
            if self.os_type == 'linux':
                print("    sudo apt-get install ngspice")
            elif self.os_type == 'darwin':
                print("    brew install ngspice")
            else:
                print("    Download from: http://ngspice.sourceforge.net/download.html")
        
        if any('kicad' in issue.lower() for issue in issues):
            print("  - Install KiCad:")
            if self.os_type == 'linux':
                print("    sudo apt-get install kicad")
            elif self.os_type == 'darwin':
                print("    brew install --cask kicad")
            else:
                print("    Download from: https://www.kicad.org/download/")
    
    def get_system_info(self) -> Dict[str, str]:
        """
        Get system information for debugging.
        
        Returns:
            Dict[str, str]: Dictionary of system information
        """
        info = {
            'os': self.os_type,
            'os_version': platform.version(),
            'platform': platform.platform(),
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'python_implementation': platform.python_implementation(),
            'architecture': platform.machine()
        }
        
        return info
    
    def generate_dependency_report(self) -> str:
        """
        Generate a comprehensive dependency report.
        
        Returns:
            str: Formatted dependency report
        """
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("DEPENDENCY CHECK REPORT")
        report_lines.append("=" * 70)
        
        # System information
        report_lines.append("\nSystem Information:")
        report_lines.append("-" * 70)
        sys_info = self.get_system_info()
        for key, value in sys_info.items():
            report_lines.append(f"  {key:20s}: {value}")
        
        # Check all tools
        report_lines.append("\n" + "-" * 70)
        report_lines.append("Dependency Status:")
        report_lines.append("-" * 70)
        
        all_issues = self.check_all_tools()
        
        for tool, issues in all_issues.items():
            status = "✓ OK" if not issues else f"✗ {len(issues)} issue(s)"
            report_lines.append(f"\n  {tool.upper():15s}: {status}")
            
            if issues:
                for issue in issues:
                    report_lines.append(f"    - {issue}")
        
        report_lines.append("\n" + "=" * 70)
        
        return "\n".join(report_lines)


def check_dependencies(tool_name: str) -> List[str]:
    """
    Convenience function to check dependencies for a tool.
    
    Args:
        tool_name (str): Name of the tool
        
    Returns:
        List[str]: List of dependency issues
    """
    checker = DependencyChecker()
    return checker.check_dependencies(tool_name)


def report_dependency_issues(issues: List[str]):
    """
    Convenience function to report dependency issues.
    
    Args:
        issues (List[str]): List of issues to report
    """
    checker = DependencyChecker()
    checker.report_dependency_issues(issues)


if __name__ == "__main__":
    # Demo usage
    checker = DependencyChecker()
    
    print("Checking dependencies for eSim Tool Manager...")
    print("\nSystem Information:")
    sys_info = checker.get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Checking all tools...")
    print("=" * 60)
    
    all_issues = checker.check_all_tools()
    
    for tool, issues in all_issues.items():
        print(f"\n{tool.upper()}:")
        if issues:
            print(f"  Found {len(issues)} issue(s):")
            for issue in issues:
                print(f"    - {issue}")
        else:
            print("  ✓ All dependencies satisfied")

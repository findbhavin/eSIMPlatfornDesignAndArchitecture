"""
Tool Installation Management Module

This module handles the installation, version management, and detection of eSim-related tools
such as Ngspice and KiCad. It automatically detects the operating system and uses appropriate
installation methods.

Author: eSim Tool Manager Team
License: MIT
"""

import os
import sys
import platform
import subprocess
import logging
import requests
from typing import Dict, Optional, Tuple
from packaging import version

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ToolInstaller:
    """
    Manages installation and version checking for eSim-related tools.
    
    Attributes:
        os_type (str): Detected operating system type
        installed_tools (Dict[str, str]): Dictionary of installed tools and their versions
    """
    
    def __init__(self):
        """Initialize the ToolInstaller with OS detection."""
        self.os_type = self._detect_os()
        self.installed_tools: Dict[str, str] = {}
        logger.info(f"ToolInstaller initialized for {self.os_type}")
    
    def _detect_os(self) -> str:
        """
        Detect the operating system type.
        
        Returns:
            str: Operating system type ('linux', 'windows', 'darwin')
        """
        system = platform.system().lower()
        logger.debug(f"Detected OS: {system}")
        return system
    
    def _run_command(self, command: list, capture_output: bool = True) -> Tuple[bool, str]:
        """
        Execute a shell command and return the result.
        
        Args:
            command (list): Command to execute as a list of strings
            capture_output (bool): Whether to capture the command output
            
        Returns:
            Tuple[bool, str]: Success status and output/error message
        """
        try:
            if capture_output:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    return True, result.stdout.strip()
                else:
                    return False, result.stderr.strip()
            else:
                result = subprocess.run(command, timeout=300)
                return result.returncode == 0, ""
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out: {' '.join(command)}")
            return False, "Command timed out"
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return False, str(e)
    
    def _check_version_command(self, tool_name: str) -> Optional[str]:
        """
        Check if a tool is installed by running its version command.
        
        Args:
            tool_name (str): Name of the tool to check
            
        Returns:
            Optional[str]: Version string if found, None otherwise
        """
        version_commands = {
            'ngspice': ['ngspice', '--version'],
            'kicad': ['kicad-cli', '--version'] if self.os_type != 'windows' else ['kicad', '--version'],
        }
        
        if tool_name.lower() not in version_commands:
            logger.warning(f"Unknown tool: {tool_name}")
            return None
        
        command = version_commands[tool_name.lower()]
        success, output = self._run_command(command)
        
        if success:
            # Parse version from output
            lines = output.split('\n')
            for line in lines:
                if 'version' in line.lower() or any(char.isdigit() for char in line):
                    # Extract version number using simple parsing
                    import re
                    version_match = re.search(r'(\d+\.?\d*\.?\d*)', line)
                    if version_match:
                        return version_match.group(1)
            return "unknown"
        
        return None
    
    def get_installed_tools(self) -> Dict[str, str]:
        """
        Get dictionary of all installed tools and their versions.
        
        Returns:
            Dict[str, str]: Dictionary mapping tool names to version strings
            
        Example:
            >>> installer = ToolInstaller()
            >>> tools = installer.get_installed_tools()
            >>> print(tools)
            {'ngspice': '40', 'kicad': '7.0.0'}
        """
        tools_to_check = ['ngspice', 'kicad']
        self.installed_tools = {}
        
        for tool in tools_to_check:
            tool_version = self._check_version_command(tool)
            if tool_version:
                self.installed_tools[tool] = tool_version
                logger.info(f"Found {tool} version {tool_version}")
            else:
                logger.info(f"{tool} not found")
        
        return self.installed_tools
    
    def is_tool_installed(self, tool_name: str) -> bool:
        """
        Check if a specific tool is installed.
        
        Args:
            tool_name (str): Name of the tool to check
            
        Returns:
            bool: True if tool is installed, False otherwise
        """
        tool_version = self._check_version_command(tool_name)
        return tool_version is not None
    
    def install_tool(self, tool_name: str, target_version: str = "latest", 
                     os_type: Optional[str] = None) -> bool:
        """
        Install a tool with the specified version.
        
        Args:
            tool_name (str): Name of the tool to install ('ngspice' or 'kicad')
            target_version (str): Version to install (default: 'latest')
            os_type (Optional[str]): Override OS type detection
            
        Returns:
            bool: True if installation succeeded, False otherwise
            
        Example:
            >>> installer = ToolInstaller()
            >>> success = installer.install_tool('ngspice', '40')
            >>> print(f"Installation {'succeeded' if success else 'failed'}")
        """
        os_type = os_type or self.os_type
        tool_name_lower = tool_name.lower()
        
        logger.info(f"Attempting to install {tool_name} version {target_version} on {os_type}")
        
        # Check if already installed
        current_version = self._check_version_command(tool_name_lower)
        if current_version and target_version != "latest":
            try:
                if version.parse(current_version) >= version.parse(target_version):
                    logger.info(f"{tool_name} {current_version} is already installed (>= {target_version})")
                    return True
            except Exception as e:
                logger.warning(f"Could not compare versions: {e}")
        
        # Installation logic based on OS and tool
        if os_type == 'linux':
            return self._install_linux(tool_name_lower, target_version)
        elif os_type == 'windows':
            return self._install_windows(tool_name_lower, target_version)
        elif os_type == 'darwin':
            return self._install_macos(tool_name_lower, target_version)
        else:
            logger.error(f"Unsupported OS: {os_type}")
            return False
    
    def _install_linux(self, tool_name: str, target_version: str) -> bool:
        """
        Install tool on Linux using apt-get or download.
        
        Args:
            tool_name (str): Name of the tool
            target_version (str): Version to install
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Installing {tool_name} on Linux")
        
        # Try package manager first
        if tool_name == 'ngspice':
            # Check if we have sudo access
            success, _ = self._run_command(['sudo', '-n', 'true'])
            if success:
                logger.info("Installing ngspice via apt-get...")
                success, output = self._run_command(
                    ['sudo', 'apt-get', 'install', '-y', 'ngspice'],
                    capture_output=True
                )
                if success:
                    logger.info("ngspice installed successfully via apt-get")
                    return True
                else:
                    logger.warning(f"apt-get installation failed: {output}")
            else:
                logger.warning("No sudo access available for package installation")
                logger.info("Please install ngspice manually: sudo apt-get install ngspice")
                return False
        
        elif tool_name == 'kicad':
            # Check if we have sudo access
            success, _ = self._run_command(['sudo', '-n', 'true'])
            if success:
                logger.info("Installing KiCad via apt-get...")
                success, output = self._run_command(
                    ['sudo', 'apt-get', 'install', '-y', 'kicad'],
                    capture_output=True
                )
                if success:
                    logger.info("KiCad installed successfully via apt-get")
                    return True
                else:
                    logger.warning(f"apt-get installation failed: {output}")
            else:
                logger.warning("No sudo access available for package installation")
                logger.info("Please install KiCad manually: sudo apt-get install kicad")
                return False
        
        return False
    
    def _install_windows(self, tool_name: str, target_version: str) -> bool:
        """
        Install tool on Windows.
        
        Args:
            tool_name (str): Name of the tool
            target_version (str): Version to install
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Installing {tool_name} on Windows")
        
        if tool_name == 'ngspice':
            logger.info("For Windows, please download ngspice from: http://ngspice.sourceforge.net/download.html")
            logger.info("Recommended: Install via the Windows installer package")
        elif tool_name == 'kicad':
            logger.info("For Windows, please download KiCad from: https://www.kicad.org/download/windows/")
            logger.info("Recommended: Install via the official Windows installer")
        
        # Windows installation typically requires manual download and installation
        # or using package managers like chocolatey
        logger.warning("Automatic installation on Windows requires manual setup or chocolatey")
        return False
    
    def _install_macos(self, tool_name: str, target_version: str) -> bool:
        """
        Install tool on macOS using brew.
        
        Args:
            tool_name (str): Name of the tool
            target_version (str): Version to install
            
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Installing {tool_name} on macOS")
        
        # Check if brew is available
        success, _ = self._run_command(['which', 'brew'])
        if not success:
            logger.error("Homebrew not found. Please install from https://brew.sh")
            return False
        
        if tool_name == 'ngspice':
            logger.info("Installing ngspice via Homebrew...")
            success, output = self._run_command(['brew', 'install', 'ngspice'])
            if success:
                logger.info("ngspice installed successfully")
                return True
            else:
                logger.error(f"Homebrew installation failed: {output}")
                return False
        
        elif tool_name == 'kicad':
            logger.info("Installing KiCad via Homebrew cask...")
            success, output = self._run_command(['brew', 'install', '--cask', 'kicad'])
            if success:
                logger.info("KiCad installed successfully")
                return True
            else:
                logger.error(f"Homebrew installation failed: {output}")
                return False
        
        return False
    
    def verify_installation(self, tool_name: str, expected_version: Optional[str] = None) -> bool:
        """
        Verify that a tool is properly installed and optionally check its version.
        
        Args:
            tool_name (str): Name of the tool to verify
            expected_version (Optional[str]): Expected version string
            
        Returns:
            bool: True if verification succeeded, False otherwise
        """
        actual_version = self._check_version_command(tool_name)
        
        if not actual_version:
            logger.error(f"{tool_name} is not installed or not in PATH")
            return False
        
        if expected_version and expected_version != "latest":
            try:
                if version.parse(actual_version) < version.parse(expected_version):
                    logger.warning(
                        f"{tool_name} version {actual_version} is older than "
                        f"expected {expected_version}"
                    )
                    return False
            except Exception as e:
                logger.warning(f"Could not compare versions: {e}")
        
        logger.info(f"{tool_name} version {actual_version} verified successfully")
        return True


def install_tool(tool_name: str, target_version: str = "latest", 
                 os_type: Optional[str] = None) -> bool:
    """
    Convenience function to install a tool.
    
    Args:
        tool_name (str): Name of the tool to install
        target_version (str): Version to install (default: 'latest')
        os_type (Optional[str]): Override OS type detection
        
    Returns:
        bool: True if installation succeeded, False otherwise
    """
    installer = ToolInstaller()
    return installer.install_tool(tool_name, target_version, os_type)


def get_installed_tools() -> Dict[str, str]:
    """
    Convenience function to get all installed tools.
    
    Returns:
        Dict[str, str]: Dictionary mapping tool names to version strings
    """
    installer = ToolInstaller()
    return installer.get_installed_tools()


if __name__ == "__main__":
    # Demo usage
    installer = ToolInstaller()
    print(f"Operating System: {installer.os_type}")
    print("\nChecking installed tools...")
    tools = installer.get_installed_tools()
    
    if tools:
        print("\nInstalled tools:")
        for tool, ver in tools.items():
            print(f"  - {tool}: {ver}")
    else:
        print("\nNo tools found installed")

"""
Update and Upgrade System Module

This module handles checking for updates, performing updates, and logging update operations
for eSim-related tools.

Author: eSim Tool Manager Team
License: MIT
"""

import os
import logging
import json
import datetime
from typing import Dict, Optional, List, Tuple
from pathlib import Path
import subprocess

from installation import ToolInstaller

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ToolUpdater:
    """
    Manages updates and upgrades for eSim-related tools.
    
    Attributes:
        installer (ToolInstaller): Tool installer instance
        log_file (Path): Path to the update log file
        update_history (List[Dict]): History of update operations
    """
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize the ToolUpdater.
        
        Args:
            log_file (Optional[str]): Path to log file (default: tool_manager/logs/updates.json)
        """
        self.installer = ToolInstaller()
        
        # Setup log file
        if log_file:
            self.log_file = Path(log_file)
        else:
            log_dir = Path(__file__).parent / 'logs'
            log_dir.mkdir(exist_ok=True)
            self.log_file = log_dir / 'updates.json'
        
        self.update_history = self._load_history()
        logger.info(f"ToolUpdater initialized with log file: {self.log_file}")
    
    def _load_history(self) -> List[Dict]:
        """
        Load update history from the log file.
        
        Returns:
            List[Dict]: List of update history entries
        """
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading update history: {e}")
                return []
        return []
    
    def _save_history(self):
        """Save update history to the log file."""
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, 'w') as f:
                json.dump(self.update_history, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving update history: {e}")
    
    def log_action(self, action: str, status: str, tool_name: str, 
                   details: Optional[str] = None):
        """
        Log an update action with timestamp.
        
        Args:
            action (str): Type of action (e.g., 'update', 'check', 'rollback')
            status (str): Status of the action ('success', 'failure', 'pending')
            tool_name (str): Name of the tool
            details (Optional[str]): Additional details about the action
            
        Example:
            >>> updater = ToolUpdater()
            >>> updater.log_action('update', 'success', 'ngspice', 'Updated to version 40')
        """
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'action': action,
            'status': status,
            'tool_name': tool_name,
            'details': details or ''
        }
        
        self.update_history.append(log_entry)
        self._save_history()
        
        log_msg = f"[{action.upper()}] {tool_name}: {status}"
        if details:
            log_msg += f" - {details}"
        
        if status == 'success':
            logger.info(log_msg)
        elif status == 'failure':
            logger.error(log_msg)
        else:
            logger.warning(log_msg)
    
    def get_latest_version_info(self, tool_name: str) -> Optional[Dict]:
        """
        Get information about the latest available version of a tool.
        
        Args:
            tool_name (str): Name of the tool
            
        Returns:
            Optional[Dict]: Dictionary with version info or None if unavailable
            
        Note:
            In a production environment, this would query online repositories
            or APIs to get the latest version information.
        """
        tool_name_lower = tool_name.lower()
        
        # Version information would typically be fetched from:
        # - ngspice: http://ngspice.sourceforge.net/download.html
        # - kicad: https://www.kicad.org/download/
        # For now, we'll provide placeholder information
        
        version_info = {
            'ngspice': {
                'latest_version': '42',
                'release_date': '2024-01-15',
                'download_url': 'http://ngspice.sourceforge.net/download.html',
                'notes': 'Latest stable release'
            },
            'kicad': {
                'latest_version': '8.0.0',
                'release_date': '2024-02-01',
                'download_url': 'https://www.kicad.org/download/',
                'notes': 'Latest stable release'
            }
        }
        
        if tool_name_lower in version_info:
            logger.debug(f"Retrieved version info for {tool_name}: {version_info[tool_name_lower]}")
            return version_info[tool_name_lower]
        else:
            logger.warning(f"No version information available for {tool_name}")
            return None
    
    def check_for_updates(self, tool_name: str) -> bool:
        """
        Check if updates are available for a tool.
        
        Args:
            tool_name (str): Name of the tool to check
            
        Returns:
            bool: True if updates are available, False otherwise
            
        Example:
            >>> updater = ToolUpdater()
            >>> if updater.check_for_updates('ngspice'):
            ...     print("Update available!")
        """
        logger.info(f"Checking for updates for {tool_name}")
        
        # Get current version
        current_version = self.installer._check_version_command(tool_name)
        if not current_version:
            logger.warning(f"{tool_name} is not installed")
            self.log_action('check', 'failure', tool_name, 'Tool not installed')
            return False
        
        # Get latest version
        latest_info = self.get_latest_version_info(tool_name)
        if not latest_info:
            logger.warning(f"Could not retrieve latest version info for {tool_name}")
            self.log_action('check', 'failure', tool_name, 'Version info unavailable')
            return False
        
        latest_version = latest_info['latest_version']
        
        try:
            from packaging import version
            current_ver = version.parse(current_version)
            latest_ver = version.parse(latest_version)
            
            if latest_ver > current_ver:
                msg = f"Update available: {current_version} -> {latest_version}"
                logger.info(f"{tool_name}: {msg}")
                self.log_action('check', 'success', tool_name, msg)
                return True
            else:
                msg = f"Already up to date (version {current_version})"
                logger.info(f"{tool_name}: {msg}")
                self.log_action('check', 'success', tool_name, msg)
                return False
        except Exception as e:
            logger.error(f"Error comparing versions: {e}")
            self.log_action('check', 'failure', tool_name, f'Version comparison error: {e}')
            return False
    
    def update_tool(self, tool_name: str, target_version: str = "latest") -> bool:
        """
        Update a tool to the specified version.
        
        Args:
            tool_name (str): Name of the tool to update
            target_version (str): Version to update to (default: 'latest')
            
        Returns:
            bool: True if update succeeded, False otherwise
            
        Example:
            >>> updater = ToolUpdater()
            >>> success = updater.update_tool('ngspice')
            >>> print(f"Update {'succeeded' if success else 'failed'}")
        """
        logger.info(f"Updating {tool_name} to version {target_version}")
        
        # Get current version for backup/rollback
        current_version = self.installer._check_version_command(tool_name)
        if current_version:
            logger.info(f"Current version of {tool_name}: {current_version}")
        
        # Backup current state
        backup_info = {
            'tool': tool_name,
            'version': current_version,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Attempt update
        try:
            success = self.installer.install_tool(tool_name, target_version)
            
            if success:
                new_version = self.installer._check_version_command(tool_name)
                msg = f"Updated from {current_version} to {new_version}"
                logger.info(msg)
                self.log_action('update', 'success', tool_name, msg)
                return True
            else:
                msg = f"Update failed"
                logger.error(msg)
                self.log_action('update', 'failure', tool_name, msg)
                return False
                
        except Exception as e:
            msg = f"Update error: {str(e)}"
            logger.error(msg)
            self.log_action('update', 'failure', tool_name, msg)
            return False
    
    def update_all_tools(self) -> Dict[str, bool]:
        """
        Update all installed tools that have updates available.
        
        Returns:
            Dict[str, bool]: Dictionary mapping tool names to update success status
            
        Example:
            >>> updater = ToolUpdater()
            >>> results = updater.update_all_tools()
            >>> for tool, success in results.items():
            ...     print(f"{tool}: {'Success' if success else 'Failed'}")
        """
        logger.info("Checking for updates for all installed tools")
        
        installed_tools = self.installer.get_installed_tools()
        results = {}
        
        for tool_name in installed_tools:
            logger.info(f"Checking {tool_name}...")
            if self.check_for_updates(tool_name):
                logger.info(f"Update available for {tool_name}, updating...")
                results[tool_name] = self.update_tool(tool_name)
            else:
                logger.info(f"{tool_name} is already up to date")
                results[tool_name] = True  # Already up to date counts as success
        
        return results
    
    def get_update_history(self, tool_name: Optional[str] = None, 
                          limit: Optional[int] = None) -> List[Dict]:
        """
        Get update history for all tools or a specific tool.
        
        Args:
            tool_name (Optional[str]): Filter by tool name
            limit (Optional[int]): Limit number of entries returned
            
        Returns:
            List[Dict]: List of update history entries
            
        Example:
            >>> updater = ToolUpdater()
            >>> history = updater.get_update_history('ngspice', limit=10)
            >>> for entry in history:
            ...     print(f"{entry['timestamp']}: {entry['action']} - {entry['status']}")
        """
        history = self.update_history
        
        if tool_name:
            history = [entry for entry in history if entry['tool_name'] == tool_name]
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def rollback_update(self, tool_name: str) -> bool:
        """
        Attempt to rollback to the previous version of a tool.
        
        Args:
            tool_name (str): Name of the tool to rollback
            
        Returns:
            bool: True if rollback succeeded, False otherwise
            
        Note:
            This is a placeholder implementation. Full rollback would require
            maintaining backup copies of previous installations.
        """
        logger.info(f"Attempting rollback for {tool_name}")
        
        # Find the last successful update for this tool
        tool_history = [entry for entry in self.update_history 
                       if entry['tool_name'] == tool_name and entry['action'] == 'update']
        
        if not tool_history:
            logger.error(f"No update history found for {tool_name}")
            self.log_action('rollback', 'failure', tool_name, 'No update history')
            return False
        
        # In a production system, we would restore from a backup
        # For now, we'll just log the attempt
        logger.warning("Rollback functionality requires backup system - not fully implemented")
        self.log_action('rollback', 'failure', tool_name, 
                       'Rollback not fully implemented - requires backup system')
        return False
    
    def clear_history(self):
        """Clear all update history logs."""
        self.update_history = []
        self._save_history()
        logger.info("Update history cleared")


def check_for_updates(tool_name: str) -> bool:
    """
    Convenience function to check for updates.
    
    Args:
        tool_name (str): Name of the tool to check
        
    Returns:
        bool: True if updates are available, False otherwise
    """
    updater = ToolUpdater()
    return updater.check_for_updates(tool_name)


def update_tool(tool_name: str, target_version: str = "latest") -> bool:
    """
    Convenience function to update a tool.
    
    Args:
        tool_name (str): Name of the tool to update
        target_version (str): Version to update to
        
    Returns:
        bool: True if update succeeded, False otherwise
    """
    updater = ToolUpdater()
    return updater.update_tool(tool_name, target_version)


def log_action(action: str, status: str, tool_name: str, details: Optional[str] = None):
    """
    Convenience function to log an action.
    
    Args:
        action (str): Type of action
        status (str): Status of the action
        tool_name (str): Name of the tool
        details (Optional[str]): Additional details
    """
    updater = ToolUpdater()
    updater.log_action(action, status, tool_name, details)


if __name__ == "__main__":
    # Demo usage
    updater = ToolUpdater()
    
    print("Checking for updates...")
    tools = ['ngspice', 'kicad']
    
    for tool in tools:
        print(f"\n{tool}:")
        has_update = updater.check_for_updates(tool)
        if has_update:
            print(f"  Update available!")
        else:
            print(f"  Already up to date")
    
    print("\nUpdate history (last 5 entries):")
    for entry in updater.get_update_history(limit=5):
        print(f"  {entry['timestamp']}: {entry['tool_name']} - {entry['action']} ({entry['status']})")

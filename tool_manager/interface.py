"""
User Interface Module

This module provides a command-line interface for the eSim Tool Manager using Click.

Author: eSim Tool Manager Team
License: MIT
"""

import sys
import click
from colorama import init, Fore, Style
import logging
from typing import Optional

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Import our modules
from installation import ToolInstaller, get_installed_tools, install_tool
from update import ToolUpdater, check_for_updates, update_tool
from config import ConfigManager, configure_tool
from dependency import DependencyChecker, check_dependencies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.CYAN}{title.center(70)}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def print_success(message: str):
    """Print a success message."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print an error message."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"{Fore.YELLOW}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print an info message."""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


@click.group()
@click.version_option(version='1.0.0', prog_name='eSim Tool Manager')
def cli():
    """
    eSim Tool Manager - Automated tool installation and management for eSim.
    
    Manage installation, updates, configuration, and dependencies for eSim-related tools
    including Ngspice and KiCad.
    """
    pass


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
def list(verbose):
    """List all installed tools and their versions."""
    print_header("Installed Tools")
    
    try:
        installer = ToolInstaller()
        tools = installer.get_installed_tools()
        
        if not tools:
            print_warning("No tools found installed")
            print_info("Use 'install' command to install tools")
            return
        
        print(f"Found {len(tools)} installed tool(s):\n")
        
        for tool_name, version in tools.items():
            print(f"  {Fore.GREEN}●{Style.RESET_ALL} {tool_name:15s} {Fore.CYAN}v{version}{Style.RESET_ALL}")
            
            if verbose:
                # Check for updates
                updater = ToolUpdater()
                has_update = updater.check_for_updates(tool_name)
                if has_update:
                    print(f"    {Fore.YELLOW}↑ Update available{Style.RESET_ALL}")
        
        print()
        
    except Exception as e:
        print_error(f"Error listing tools: {e}")
        logger.exception("Error in list command")
        sys.exit(1)


@cli.command()
@click.argument('tool')
@click.option('--version', '-v', default='latest', help='Specific version to install')
@click.option('--force', '-f', is_flag=True, help='Force reinstall even if already installed')
def install(tool, version, force):
    """Install a tool (ngspice or kicad)."""
    print_header(f"Installing {tool}")
    
    try:
        installer = ToolInstaller()
        
        # Check if already installed
        if not force:
            current_version = installer._check_version_command(tool)
            if current_version:
                print_info(f"{tool} is already installed (version {current_version})")
                if click.confirm('Do you want to reinstall?', default=False):
                    force = True
                else:
                    return
        
        print_info(f"Installing {tool} (version: {version})...")
        
        success = installer.install_tool(tool, version)
        
        if success:
            print_success(f"Successfully installed {tool}")
            
            # Verify installation
            new_version = installer._check_version_command(tool)
            if new_version:
                print_info(f"Installed version: {new_version}")
        else:
            print_error(f"Failed to install {tool}")
            print_info("Please check the logs for more details")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Error during installation: {e}")
        logger.exception("Error in install command")
        sys.exit(1)


@cli.command()
@click.argument('tool', required=False)
@click.option('--all', '-a', 'update_all', is_flag=True, help='Update all tools')
@click.option('--check-only', '-c', is_flag=True, help='Only check for updates')
def update(tool, update_all, check_only):
    """Update a tool or check for updates."""
    print_header("Tool Updates")
    
    try:
        updater = ToolUpdater()
        
        if update_all:
            print_info("Checking all tools for updates...")
            results = updater.update_all_tools()
            
            print("\nUpdate Results:")
            for tool_name, success in results.items():
                if success:
                    print_success(f"{tool_name} updated successfully")
                else:
                    print_error(f"{tool_name} update failed")
        
        elif tool:
            if check_only:
                print_info(f"Checking for updates for {tool}...")
                has_update = updater.check_for_updates(tool)
                
                if has_update:
                    print_warning(f"Update available for {tool}")
                    if click.confirm('Do you want to update now?', default=True):
                        success = updater.update_tool(tool)
                        if success:
                            print_success(f"Successfully updated {tool}")
                        else:
                            print_error(f"Failed to update {tool}")
                else:
                    print_success(f"{tool} is already up to date")
            else:
                print_info(f"Updating {tool}...")
                success = updater.update_tool(tool)
                
                if success:
                    print_success(f"Successfully updated {tool}")
                else:
                    print_error(f"Failed to update {tool}")
        else:
            print_error("Please specify a tool or use --all flag")
            print_info("Usage: update <tool> or update --all")
            sys.exit(1)
            
    except Exception as e:
        print_error(f"Error during update: {e}")
        logger.exception("Error in update command")
        sys.exit(1)


@cli.command()
@click.argument('tool', required=False)
@click.option('--all', '-a', 'check_all', is_flag=True, help='Check all tools')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed report')
def check(tool, check_all, verbose):
    """Check dependencies for tools."""
    print_header("Dependency Check")
    
    try:
        checker = DependencyChecker()
        
        if check_all or not tool:
            # Check all tools
            print_info("Checking dependencies for all tools...")
            all_issues = checker.check_all_tools()
            
            print()
            for tool_name, issues in all_issues.items():
                if issues:
                    print(f"{Fore.YELLOW}●{Style.RESET_ALL} {tool_name:15s} {Fore.RED}{len(issues)} issue(s){Style.RESET_ALL}")
                    if verbose:
                        for issue in issues:
                            print(f"    - {issue}")
                else:
                    print(f"{Fore.GREEN}●{Style.RESET_ALL} {tool_name:15s} {Fore.GREEN}OK{Style.RESET_ALL}")
            
            # Count total issues
            total_issues = sum(len(issues) for issues in all_issues.values())
            print()
            if total_issues > 0:
                print_warning(f"Found {total_issues} total issue(s)")
                print_info("Run with --verbose for details")
            else:
                print_success("All dependencies satisfied!")
        else:
            # Check specific tool
            print_info(f"Checking dependencies for {tool}...")
            issues = checker.check_dependencies(tool)
            
            if issues:
                print()
                checker.report_dependency_issues(issues)
            else:
                print_success(f"All dependencies satisfied for {tool}")
    
    except Exception as e:
        print_error(f"Error checking dependencies: {e}")
        logger.exception("Error in check command")
        sys.exit(1)


@cli.command()
@click.argument('tool')
@click.option('--enable/--disable', default=None, help='Enable or disable the tool')
@click.option('--auto-update/--no-auto-update', default=None, help='Enable or disable auto-updates')
@click.option('--path', help='Set the tool installation path')
def config(tool, enable, auto_update, path):
    """Configure a tool."""
    print_header(f"Configuring {tool}")
    
    try:
        config_mgr = ConfigManager()
        settings = {}
        
        if enable is not None:
            settings['enabled'] = enable
            print_info(f"{'Enabling' if enable else 'Disabling'} {tool}")
        
        if auto_update is not None:
            settings['auto_update'] = auto_update
            print_info(f"{'Enabling' if auto_update else 'Disabling'} auto-updates for {tool}")
        
        if path:
            settings['path'] = path
            print_info(f"Setting path for {tool}: {path}")
        
        if not settings:
            # Show current configuration
            print(f"\nCurrent configuration for {tool}:")
            print(f"  Enabled: {config_mgr.get(f'tools.{tool}.enabled', 'Not set')}")
            print(f"  Auto-update: {config_mgr.get(f'tools.{tool}.auto_update', 'Not set')}")
            print(f"  Path: {config_mgr.get(f'tools.{tool}.path', 'Not set')}")
        else:
            success = config_mgr.configure_tool(tool, settings)
            
            if success:
                print_success(f"Configuration updated for {tool}")
            else:
                print_error(f"Failed to update configuration for {tool}")
    
    except Exception as e:
        print_error(f"Error configuring tool: {e}")
        logger.exception("Error in config command")
        sys.exit(1)


@cli.command()
@click.option('--limit', '-n', default=10, help='Number of log entries to show')
@click.option('--tool', help='Filter logs by tool name')
def logs(limit, tool):
    """Show action logs."""
    print_header("Action Logs")
    
    try:
        updater = ToolUpdater()
        history = updater.get_update_history(tool_name=tool, limit=limit)
        
        if not history:
            print_warning("No logs found")
            return
        
        print(f"Showing last {len(history)} log entries:\n")
        
        for entry in reversed(history):
            timestamp = entry.get('timestamp', 'N/A')
            action = entry.get('action', 'N/A')
            status = entry.get('status', 'N/A')
            tool_name = entry.get('tool_name', 'N/A')
            details = entry.get('details', '')
            
            # Color based on status
            if status == 'success':
                status_color = Fore.GREEN
            elif status == 'failure':
                status_color = Fore.RED
            else:
                status_color = Fore.YELLOW
            
            print(f"{Fore.CYAN}{timestamp[:19]}{Style.RESET_ALL} | "
                  f"{tool_name:10s} | "
                  f"{action:12s} | "
                  f"{status_color}{status:10s}{Style.RESET_ALL}")
            
            if details:
                print(f"  └─ {details}")
        
        print()
        
    except Exception as e:
        print_error(f"Error reading logs: {e}")
        logger.exception("Error in logs command")
        sys.exit(1)


@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
def status(verbose):
    """Show status of all tools and system."""
    print_header("eSim Tool Manager Status")
    
    try:
        # System info
        checker = DependencyChecker()
        sys_info = checker.get_system_info()
        
        print(f"{Fore.CYAN}System Information:{Style.RESET_ALL}")
        print(f"  OS: {sys_info['os']} ({sys_info['platform']})")
        print(f"  Python: {sys_info['python_version']}")
        print()
        
        # Installed tools
        print(f"{Fore.CYAN}Installed Tools:{Style.RESET_ALL}")
        installer = ToolInstaller()
        tools = installer.get_installed_tools()
        
        if tools:
            for tool_name, version in tools.items():
                print(f"  {Fore.GREEN}●{Style.RESET_ALL} {tool_name:15s} v{version}")
        else:
            print(f"  {Fore.YELLOW}No tools installed{Style.RESET_ALL}")
        print()
        
        # Configuration
        print(f"{Fore.CYAN}Configuration:{Style.RESET_ALL}")
        config_mgr = ConfigManager()
        print(f"  Config file: {config_mgr.config_file}")
        print(f"  Auto-update: {config_mgr.get('update.check_on_startup', False)}")
        print()
        
        # Dependency status (brief)
        if verbose:
            print(f"{Fore.CYAN}Dependency Status:{Style.RESET_ALL}")
            all_issues = checker.check_all_tools()
            for tool_name, issues in all_issues.items():
                status_text = "OK" if not issues else f"{len(issues)} issue(s)"
                status_color = Fore.GREEN if not issues else Fore.RED
                print(f"  {tool_name:15s} {status_color}{status_text}{Style.RESET_ALL}")
        
    except Exception as e:
        print_error(f"Error getting status: {e}")
        logger.exception("Error in status command")
        sys.exit(1)


def main_menu():
    """
    Display the main menu (for interactive mode).
    
    This is an alternative to the CLI for users who prefer an interactive interface.
    """
    print_header("eSim Tool Manager - Interactive Mode")
    
    while True:
        print("\nAvailable commands:")
        print("  1. List installed tools")
        print("  2. Install a tool")
        print("  3. Update tools")
        print("  4. Check dependencies")
        print("  5. Configure tools")
        print("  6. View logs")
        print("  7. Show status")
        print("  0. Exit")
        
        choice = input(f"\n{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")
        
        try:
            if choice == '0':
                print_info("Goodbye!")
                break
            elif choice == '1':
                cli(['list'])
            elif choice == '2':
                tool = input("Enter tool name (ngspice/kicad): ")
                cli(['install', tool])
            elif choice == '3':
                tool = input("Enter tool name (or press Enter for all): ")
                if tool:
                    cli(['update', tool])
                else:
                    cli(['update', '--all'])
            elif choice == '4':
                cli(['check', '--all'])
            elif choice == '5':
                tool = input("Enter tool name: ")
                cli(['config', tool])
            elif choice == '6':
                cli(['logs'])
            elif choice == '7':
                cli(['status', '--verbose'])
            else:
                print_warning("Invalid choice, please try again")
        except Exception as e:
            print_error(f"Error: {e}")


if __name__ == "__main__":
    # If run with --interactive flag, show menu instead of CLI
    if '--interactive' in sys.argv:
        sys.argv.remove('--interactive')
        main_menu()
    else:
        cli()

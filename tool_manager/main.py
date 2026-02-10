"""
eSim Tool Manager - Main Entry Point

This is the main entry point for the eSim Tool Manager application.
It provides automated tool installation, updates, configuration, and dependency management
for eSim-related tools.

Author: eSim Tool Manager Team
License: MIT
"""

import sys
import os
import logging
from pathlib import Path
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Add the current directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent))

# Import interface module
from interface import cli, print_header, print_info, print_error


def setup_logging():
    """Setup logging configuration."""
    log_dir = Path.home() / '.esim_tools' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'tool_manager.log'
    
    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return log_file


def display_banner():
    """Display welcome banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              eSim Tool Manager v1.0.0                           ║
║                                                                  ║
║  Automated Tool Installation & Management for eSim              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def check_python_version():
    """Check if Python version meets requirements."""
    required_version = (3, 7)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print_error(
            f"Python {required_version[0]}.{required_version[1]}+ is required. "
            f"Current version: {current_version[0]}.{current_version[1]}"
        )
        sys.exit(1)


def main():
    """Main entry point for the tool manager."""
    try:
        # Check Python version
        check_python_version()
        
        # Setup logging
        log_file = setup_logging()
        
        # Display banner if not in quiet mode
        if '--help' not in sys.argv and '-h' not in sys.argv:
            display_banner()
            print_info(f"Logging to: {log_file}\n")
        
        # Run the CLI
        cli()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        logging.exception("Unexpected error in main")
        sys.exit(1)


if __name__ == "__main__":
    main()

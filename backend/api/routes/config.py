"""
Configuration routes for eSim Platform API
"""
import os
import sys
from flask import Blueprint, jsonify, request

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.esim_platform.config_manager import ConfigManager

bp = Blueprint('config', __name__)

# Config file path
CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../config.yaml'))

@bp.route('/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        config_manager = ConfigManager(CONFIG_FILE if os.path.exists(CONFIG_FILE) else None)
        
        return jsonify({
            'success': True,
            'config': config_manager.config
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/config', methods=['PUT'])
def update_config():
    """Update configuration"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        config_manager = ConfigManager(CONFIG_FILE if os.path.exists(CONFIG_FILE) else None)
        
        # Update configuration values
        new_config = request.json
        
        for section, values in new_config.items():
            if section in config_manager.config:
                config_manager.config[section].update(values)
        
        # Save to file
        config_manager.save_to_file(CONFIG_FILE)
        
        return jsonify({
            'success': True,
            'config': config_manager.config
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

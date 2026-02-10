"""
Tool management routes for eSim Platform API
"""
import os
import sys
import subprocess
from flask import Blueprint, jsonify, request

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

bp = Blueprint('tools', __name__)

@bp.route('/tools', methods=['GET'])
def list_tools():
    """Get status of required tools"""
    try:
        tools_status = {
            'ngspice': check_tool_available('ngspice'),
            'python': check_tool_available('python3'),
        }
        
        return jsonify({
            'success': True,
            'tools': tools_status,
            'all_available': all(tools_status.values())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/tools/install', methods=['POST'])
def install_tool():
    """Install a tool (placeholder for future implementation)"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Request must be JSON'
            }), 400
        
        tool_name = request.json.get('tool_name')
        
        if not tool_name:
            return jsonify({
                'success': False,
                'error': 'tool_name is required'
            }), 400
        
        return jsonify({
            'success': False,
            'error': 'Tool installation not yet implemented. Please install tools manually.',
            'message': 'For ngspice: apt-get install ngspice or download from http://ngspice.sourceforge.net/'
        }), 501
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def check_tool_available(tool_name):
    """
    Check if a tool is available on the system
    
    Args:
        tool_name: Name of the tool to check
        
    Returns:
        bool: True if available, False otherwise
    """
    try:
        result = subprocess.run(
            ['which', tool_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

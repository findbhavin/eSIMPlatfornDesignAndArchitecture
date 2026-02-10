"""
Circuit routes for eSim Platform API
"""
import os
import sys
from flask import Blueprint, jsonify, request

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.esim_platform.circuit_analyzer import CircuitAnalyzer
from backend.api.utils import format_circuit_info, save_uploaded_file

bp = Blueprint('circuits', __name__)

# Path to circuits directory
CIRCUITS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../circuits'))

@bp.route('/circuits', methods=['GET'])
def list_circuits():
    """Get list of available circuits"""
    try:
        circuits = []
        
        if os.path.exists(CIRCUITS_DIR):
            for filename in os.listdir(CIRCUITS_DIR):
                if filename.endswith('.cir'):
                    circuit_path = os.path.join(CIRCUITS_DIR, filename)
                    circuits.append(format_circuit_info(circuit_path))
        
        return jsonify({
            'success': True,
            'circuits': circuits,
            'count': len(circuits)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/circuits/<circuit_id>', methods=['GET'])
def get_circuit(circuit_id):
    """Get details of a specific circuit"""
    try:
        circuit_file = os.path.join(CIRCUITS_DIR, f"{circuit_id}.cir")
        
        if not os.path.exists(circuit_file):
            return jsonify({
                'success': False,
                'error': 'Circuit not found'
            }), 404
        
        # Analyze circuit
        analyzer = CircuitAnalyzer()
        analyzer.load_netlist(circuit_file)
        analysis = analyzer.parse_netlist()
        
        # Read netlist content
        with open(circuit_file, 'r') as f:
            netlist_content = f.read()
        
        circuit_info = format_circuit_info(circuit_file, analysis)
        circuit_info['netlist'] = netlist_content
        
        return jsonify({
            'success': True,
            'circuit': circuit_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/analyze', methods=['POST'])
def analyze_circuit():
    """Analyze uploaded circuit netlist"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            # Check if netlist content was provided as text
            if 'content' in request.json:
                # Save content to temporary file
                temp_file = '/tmp/temp_circuit.cir'
                with open(temp_file, 'w') as f:
                    f.write(request.json['content'])
                netlist_path = temp_file
            else:
                return jsonify({
                    'success': False,
                    'error': 'No file or content provided'
                }), 400
        else:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': 'No file selected'
                }), 400
            
            # Save uploaded file
            netlist_path = save_uploaded_file(file, '/tmp')
            
            if not netlist_path:
                return jsonify({
                    'success': False,
                    'error': 'Invalid file type. Allowed: .cir, .sp, .net, .txt'
                }), 400
        
        # Analyze circuit
        analyzer = CircuitAnalyzer()
        analyzer.load_netlist(netlist_path)
        analysis = analyzer.parse_netlist()
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

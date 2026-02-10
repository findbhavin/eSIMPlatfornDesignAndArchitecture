"""
Simulation routes for eSim Platform API
"""
import os
import sys
import uuid
import time
from flask import Blueprint, jsonify, request

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.esim_platform.esim_wrapper import ESimWrapper
from backend.api.utils import save_uploaded_file

bp = Blueprint('simulation', __name__)

# In-memory simulation status storage (in production, use Redis or database)
simulations = {}

@bp.route('/simulate', methods=['POST'])
def run_simulation():
    """Run circuit simulation"""
    try:
        # Get netlist path from request
        netlist_path = None
        
        if 'file' in request.files:
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
                    'error': 'Invalid file type'
                }), 400
        
        elif request.is_json and 'circuit_id' in request.json:
            # Use pre-existing circuit
            circuit_id = request.json['circuit_id']
            circuits_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../circuits'))
            netlist_path = os.path.join(circuits_dir, f"{circuit_id}.cir")
            
            if not os.path.exists(netlist_path):
                return jsonify({
                    'success': False,
                    'error': 'Circuit not found'
                }), 404
        
        else:
            return jsonify({
                'success': False,
                'error': 'No circuit provided'
            }), 400
        
        # Create simulation ID
        sim_id = str(uuid.uuid4())
        
        # Initialize simulation status
        simulations[sim_id] = {
            'id': sim_id,
            'status': 'running',
            'started_at': time.time(),
            'circuit': os.path.basename(netlist_path)
        }
        
        # Run simulation
        wrapper = ESimWrapper()
        
        if not wrapper.is_esim_available():
            simulations[sim_id]['status'] = 'failed'
            simulations[sim_id]['error'] = 'ngspice not available'
            return jsonify({
                'success': False,
                'error': 'Simulation engine (ngspice) not available',
                'simulation_id': sim_id
            }), 500
        
        success, output = wrapper.simulate_circuit(netlist_path)
        
        # Update simulation status
        simulations[sim_id].update({
            'status': 'completed' if success else 'failed',
            'completed_at': time.time(),
            'output': output if success else None,
            'error': output if not success else None
        })
        
        return jsonify({
            'success': success,
            'simulation_id': sim_id,
            'status': simulations[sim_id]['status'],
            'output': output if success else None,
            'error': output if not success else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@bp.route('/simulation/<sim_id>/status', methods=['GET'])
def get_simulation_status(sim_id):
    """Get simulation status"""
    try:
        if sim_id not in simulations:
            return jsonify({
                'success': False,
                'error': 'Simulation not found'
            }), 404
        
        return jsonify({
            'success': True,
            'simulation': simulations[sim_id]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

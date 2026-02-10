"""
Utility functions for the API
"""
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'cir', 'sp', 'net', 'txt'}

def allowed_file(filename):
    """
    Check if file has allowed extension
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """
    Save uploaded file securely
    
    Args:
        file: File object from request
        upload_folder: Directory to save file
        
    Returns:
        str: Path to saved file or None if error
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filepath
    return None

def format_circuit_info(circuit_file, analysis_result=None):
    """
    Format circuit information for API response
    
    Args:
        circuit_file: Path to circuit file
        analysis_result: Optional analysis results
        
    Returns:
        dict: Formatted circuit information
    """
    circuit_id = os.path.splitext(os.path.basename(circuit_file))[0]
    
    result = {
        'id': circuit_id,
        'name': circuit_id.replace('_', ' ').title(),
        'filename': os.path.basename(circuit_file),
        'path': circuit_file
    }
    
    if analysis_result:
        result.update({
            'components': analysis_result.get('components', []),
            'nodes': analysis_result.get('nodes', []),
            'component_count': analysis_result.get('component_count', 0),
            'node_count': analysis_result.get('node_count', 0),
            'circuit_name': analysis_result.get('circuit_name', '')
        })
    
    return result

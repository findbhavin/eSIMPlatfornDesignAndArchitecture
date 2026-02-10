"""
Example: Basic Circuit Analysis

This example demonstrates how to use the CircuitAnalyzer
to load, parse, and analyze a circuit netlist.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.esim_platform import CircuitAnalyzer


def main():
    """Main function to demonstrate circuit analysis."""
    
    print("="*70)
    print("Circuit Analysis Example")
    print("="*70)
    print()
    
    # Create analyzer instance
    analyzer = CircuitAnalyzer()
    
    # Analyze voltage divider circuit
    circuit_file = 'circuits/voltage_divider.cir'
    
    print(f"Loading circuit: {circuit_file}")
    if not analyzer.load_netlist(circuit_file):
        print("Error: Could not load circuit file")
        return 1
    
    print("✓ Circuit loaded successfully")
    print()
    
    # Parse the netlist
    print("Parsing netlist...")
    circuit_info = analyzer.parse_netlist()
    
    print(f"✓ Netlist parsed")
    print()
    
    # Display circuit information
    print("Circuit Information:")
    print("-" * 70)
    print(f"  Name: {circuit_info['circuit_name']}")
    print(f"  Components: {circuit_info['component_count']}")
    print(f"  Nodes: {circuit_info['node_count']}")
    print()
    
    # Get component summary
    summary = analyzer.get_component_summary()
    print("Component Summary:")
    print("-" * 70)
    
    component_names = {
        'V': 'Voltage Sources',
        'I': 'Current Sources',
        'R': 'Resistors',
        'C': 'Capacitors',
        'L': 'Inductors',
        'D': 'Diodes',
        'Q': 'Transistors',
        'M': 'MOSFETs'
    }
    
    for comp_type, count in summary.items():
        name = component_names.get(comp_type, comp_type)
        print(f"  {name}: {count}")
    print()
    
    # Perform comprehensive analysis
    print("Performing circuit analysis...")
    analysis = analyzer.analyze_circuit()
    
    print("✓ Analysis complete")
    print()
    
    # Display detailed results
    print("Detailed Analysis:")
    print("-" * 70)
    print(f"  Circuit Name: {analysis['circuit_name']}")
    print(f"  Total Components: {analysis['total_components']}")
    print(f"  Total Nodes: {analysis['total_nodes']}")
    print()
    
    print("  Nodes:")
    for node in analysis['nodes']:
        print(f"    - {node}")
    print()
    
    print("  Components:")
    for i, comp in enumerate(analysis['components'], 1):
        print(f"    {i}. {comp['name']} ({comp['type']})")
        print(f"       Nodes: {', '.join(comp['nodes'])}")
        if comp['value']:
            print(f"       Value: {comp['value']}")
    print()
    
    # Validate circuit
    print("Validating circuit...")
    is_valid, issues = analyzer.validate_circuit()
    
    if is_valid:
        print("✓ Circuit validation passed")
    else:
        print("⚠ Circuit has issues:")
        for issue in issues:
            print(f"  - {issue}")
    
    print()
    print("="*70)
    print("Analysis completed successfully!")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

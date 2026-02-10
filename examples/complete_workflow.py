"""
Example: Complete Workflow

This example demonstrates a complete workflow:
1. Load configuration
2. Analyze circuit
3. Validate circuit
4. Run simulation
5. Process results
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.esim_platform import CircuitAnalyzer, ESimWrapper, ConfigManager


def main():
    """Main function demonstrating complete workflow."""
    
    print("="*70)
    print("Complete Workflow Example")
    print("="*70)
    print()
    
    circuit_file = 'circuits/rc_filter.cir'
    
    # Step 1: Configuration
    print("Step 1: Loading Configuration")
    print("-" * 70)
    
    config = ConfigManager()
    config.set('esim.timeout', 60)
    config.set('simulation.verbosity', 'normal')
    
    print("Configuration:")
    print(f"  Timeout: {config.get('esim.timeout')} seconds")
    print(f"  Output Dir: {config.get('simulation.output_dir')}")
    print(f"  Verbosity: {config.get('simulation.verbosity')}")
    print()
    
    # Step 2: Circuit Analysis
    print("Step 2: Analyzing Circuit")
    print("-" * 70)
    
    analyzer = CircuitAnalyzer()
    
    if not analyzer.load_netlist(circuit_file):
        print("✗ Failed to load circuit")
        return 1
    
    analyzer.parse_netlist()
    analysis = analyzer.analyze_circuit()
    
    print(f"✓ Circuit loaded: {analysis['circuit_name']}")
    print(f"  Components: {analysis['total_components']}")
    print(f"  Nodes: {analysis['total_nodes']}")
    
    # Show component summary
    summary = analysis['component_summary']
    print(f"  Summary: {', '.join(f'{k}={v}' for k, v in summary.items())}")
    print()
    
    # Step 3: Circuit Validation
    print("Step 3: Validating Circuit")
    print("-" * 70)
    
    is_valid, issues = analyzer.validate_circuit()
    
    if is_valid:
        print("✓ Circuit validation passed")
    else:
        print("⚠ Circuit has issues:")
        for issue in issues:
            print(f"  - {issue}")
    print()
    
    # Step 4: Simulation
    print("Step 4: Running Simulation")
    print("-" * 70)
    
    wrapper = ESimWrapper()
    
    if not wrapper.is_esim_available():
        print("⚠ ngspice not available, skipping simulation")
        print("  Install from: https://esim.fossee.in/downloads")
        print()
    else:
        print("Starting simulation...")
        
        success, output = wrapper.simulate_circuit(circuit_file)
        
        if success:
            print("✓ Simulation completed")
            
            # Parse results
            info = wrapper.parse_simulation_output(output)
            
            print(f"  Errors: {len(info['errors'])}")
            print(f"  Warnings: {len(info['warnings'])}")
            
            if info['warnings']:
                print("\n  Warnings:")
                for warning in info['warnings'][:3]:  # Show first 3
                    print(f"    ⚠ {warning}")
            
        else:
            print("✗ Simulation failed")
            print(f"  Error: {output[:200]}")
        
        print()
    
    # Step 5: Summary
    print("Step 5: Summary")
    print("-" * 70)
    print(f"Circuit: {circuit_file}")
    print(f"  ✓ Analysis: Complete")
    print(f"  {'✓' if is_valid else '⚠'} Validation: {'Passed' if is_valid else 'Issues found'}")
    
    if wrapper.is_esim_available():
        sim_status = "Complete" if success else "Failed"
        print(f"  {'✓' if success else '✗'} Simulation: {sim_status}")
    else:
        print(f"  ⚠ Simulation: Skipped (ngspice not available)")
    
    print()
    print("="*70)
    print("Workflow completed!")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

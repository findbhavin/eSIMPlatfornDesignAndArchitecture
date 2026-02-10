"""
Example: Circuit Simulation

This example demonstrates how to use the ESimWrapper
to run circuit simulations with ngspice.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.esim_platform import ESimWrapper


def main():
    """Main function to demonstrate circuit simulation."""
    
    print("="*70)
    print("Circuit Simulation Example")
    print("="*70)
    print()
    
    # Create wrapper instance
    wrapper = ESimWrapper()
    
    # Check if eSim/ngspice is available
    print("Checking for ngspice...")
    if not wrapper.is_esim_available():
        print("✗ ngspice not found!")
        print()
        print("Please install eSim or ngspice:")
        print("  - eSim: https://esim.fossee.in/downloads")
        print("  - ngspice: sudo apt install ngspice")
        return 1
    
    print("✓ ngspice is available")
    print()
    
    # Display wrapper status
    status = wrapper.get_simulation_status()
    print("Wrapper Status:")
    print("-" * 70)
    print(f"  eSim Path: {status['esim_path'] or 'Not set'}")
    print(f"  Available: {status['esim_available']}")
    print(f"  Simulations Run: {status['simulations_run']}")
    print()
    
    # Simulate a circuit
    circuit_file = 'circuits/voltage_divider.cir'
    
    print(f"Simulating: {circuit_file}")
    print("-" * 70)
    print("Running simulation...")
    print()
    
    success, output = wrapper.simulate_circuit(circuit_file)
    
    if success:
        print("✓ Simulation completed successfully!")
        print()
        
        # Parse simulation output
        info = wrapper.parse_simulation_output(output)
        
        print("Simulation Results:")
        print("-" * 70)
        print(f"  Success: {info['success']}")
        print(f"  Errors: {len(info['errors'])}")
        print(f"  Warnings: {len(info['warnings'])}")
        print()
        
        # Display warnings if any
        if info['warnings']:
            print("Warnings:")
            for warning in info['warnings']:
                print(f"  ⚠ {warning}")
            print()
        
        # Display errors if any
        if info['errors']:
            print("Errors:")
            for error in info['errors']:
                print(f"  ✗ {error}")
            print()
        
        # Show simulation output (first 1000 characters)
        print("Simulation Output (excerpt):")
        print("-" * 70)
        print(output[:1000])
        if len(output) > 1000:
            print(f"\n... ({len(output) - 1000} more characters)")
        print()
        
    else:
        print("✗ Simulation failed!")
        print()
        print("Error Details:")
        print("-" * 70)
        print(output)
        return 1
    
    print("="*70)
    print("Simulation completed!")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

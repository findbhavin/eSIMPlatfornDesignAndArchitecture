# Circuit Design Documentation

## Overview

This document provides detailed information about the circuit designs included in the eSim Platform project. Each circuit is designed to demonstrate key eSim capabilities and serves as a reference for circuit simulation.

## Circuit Collection

The project includes four standard circuit designs:
1. Voltage Divider Circuit
2. RC Low Pass Filter
3. Non-Inverting Operational Amplifier
4. Half-Wave Rectifier

---

## 1. Voltage Divider Circuit

### Description
A basic resistive voltage divider that demonstrates fundamental circuit analysis and DC operating point calculations.

### Circuit Schematic
```
        Vin (10V)
           │
           R1 (1kΩ)
           │
    Vout ──┤
           │
           R2 (2kΩ)
           │
          GND
```

### Components
| Component | Value | Description |
|-----------|-------|-------------|
| Vin | 10V DC | Input voltage source |
| R1 | 1kΩ | Upper resistor |
| R2 | 2kΩ | Lower resistor |

### Design Calculations

**Output Voltage**:
```
Vout = Vin × (R2 / (R1 + R2))
Vout = 10V × (2kΩ / (1kΩ + 2kΩ))
Vout = 10V × (2/3)
Vout = 6.67V
```

**Current**:
```
I = Vin / (R1 + R2)
I = 10V / 3kΩ
I = 3.33mA
```

**Power Dissipation**:
```
P_total = Vin × I = 10V × 3.33mA = 33.3mW
P_R1 = I² × R1 = (3.33mA)² × 1kΩ = 11.1mW
P_R2 = I² × R2 = (3.33mA)² × 2kΩ = 22.2mW
```

### Simulation Parameters
- **Analysis Type**: DC Operating Point, DC Sweep
- **DC Sweep Range**: 0V to 15V in 0.5V steps
- **Expected Results**:
  - Vout = 6.67V at Vin = 10V
  - Linear relationship between Vin and Vout

### File Location
`circuits/voltage_divider.cir`

### Usage
```bash
ngspice circuits/voltage_divider.cir
```

---

## 2. RC Low Pass Filter

### Description
A first-order passive RC low pass filter that demonstrates frequency response analysis and filtering characteristics.

### Circuit Schematic
```
    Vin ──R1 (1kΩ)──┬─── Vout
                     │
                    C1 (1µF)
                     │
                    GND
```

### Components
| Component | Value | Description |
|-----------|-------|-------------|
| Vin | 1V AC | AC input signal |
| R1 | 1kΩ | Series resistor |
| C1 | 1µF | Filter capacitor |
| RL | 100kΩ | Load resistor |

### Design Calculations

**Cutoff Frequency**:
```
fc = 1 / (2π × R × C)
fc = 1 / (2π × 1kΩ × 1µF)
fc = 1 / (6.283 × 10⁻³)
fc ≈ 159 Hz
```

**Transfer Function**:
```
H(jω) = 1 / (1 + jωRC)
|H(jω)| = 1 / √(1 + (ωRC)²)
```

**At Cutoff Frequency**:
```
|H(jωc)| = 1/√2 ≈ 0.707 (-3dB)
Phase = -45°
```

### Frequency Response
- **Passband**: DC to ~159 Hz (|H| ≈ 1)
- **Cutoff**: 159 Hz (|H| = -3dB)
- **Stopband**: >159 Hz (|H| decreases at -20dB/decade)
- **Phase Response**: 0° at DC, -45° at fc, -90° at high frequencies

### Simulation Parameters
- **Analysis Type**: AC Analysis
- **Frequency Range**: 1 Hz to 10 kHz
- **Points per Decade**: 20
- **Expected Results**:
  - Flat response below 159 Hz
  - -3dB point at 159 Hz
  - -20dB/decade roll-off above cutoff

### File Location
`circuits/rc_filter.cir`

### Usage
```bash
ngspice circuits/rc_filter.cir
```

---

## 3. Non-Inverting Operational Amplifier

### Description
An operational amplifier in non-inverting configuration demonstrating gain, bandwidth, and feedback principles.

### Circuit Schematic
```
        VCC (+15V)
           │
    ┌──────┴──────┐
    │             │
Vin─┤+           Out├─── Vout
    │   Op-Amp     │
  ──┤-            │
  │ │             │
  │ └──────┬──────┘
  │        │
  │       VEE (-15V)
  │
  │     R2 (10kΩ)
  └───┬────────┬───
      │        │
      R1       │
     (1kΩ)     │
      │        │
     GND      GND
```

### Components
| Component | Value | Description |
|-----------|-------|-------------|
| Vin | 1V AC | Input signal |
| VCC | +15V DC | Positive supply |
| VEE | -15V DC | Negative supply |
| R1 | 1kΩ | Feedback resistor to ground |
| R2 | 10kΩ | Feedback resistor |
| Rin | 1kΩ | Input resistor |
| RL | 10kΩ | Load resistor |

### Design Calculations

**Voltage Gain**:
```
Av = 1 + (R2 / R1)
Av = 1 + (10kΩ / 1kΩ)
Av = 11 (20.8 dB)
```

**Input Impedance**:
```
Zin ≈ ∞ (very high, >1MΩ for ideal op-amp)
```

**Output Impedance**:
```
Zout ≈ 0 (very low, <100Ω for ideal op-amp)
```

**Bandwidth**:
```
For typical op-amp with GBW = 1MHz:
BW = GBW / Av
BW = 1MHz / 11
BW ≈ 91 kHz
```

### Simulation Parameters
- **Analysis Type**: AC Analysis, Transient Analysis
- **AC Frequency Range**: 1 Hz to 1 MHz
- **Transient Time**: 10 ms
- **Expected Results**:
  - Voltage gain: 20.8 dB (factor of 11)
  - Flat frequency response within bandwidth
  - Linear amplification in time domain

### File Location
`circuits/opamp_noninverting.cir`

### Usage
```bash
ngspice circuits/opamp_noninverting.cir
```

---

## 4. Half-Wave Rectifier

### Description
A half-wave rectifier circuit that converts AC to pulsating DC, demonstrating diode behavior and filtering.

### Circuit Schematic
```
              D1
    Vin ──────┤>├──┬──── Vout
                   │
                   C1 (100µF)
                   │
                  RL (1kΩ)
                   │
                  GND
```

### Components
| Component | Value | Description |
|-----------|-------|-------------|
| Vin | 10V peak, 50Hz | AC input source (sine wave) |
| D1 | 1N4148 | Rectifier diode |
| RL | 1kΩ | Load resistor |
| C1 | 100µF | Filter capacitor |

### Design Calculations

**Without Capacitor**:
```
Vpeak = Vin_peak - Vdiode
Vpeak ≈ 10V - 0.7V = 9.3V
Vavg = Vpeak / π ≈ 2.96V
Vrms = Vpeak / 2 ≈ 4.65V
```

**With Filter Capacitor**:
```
Ripple Voltage:
Vripple = (Vout / (f × RL × C))
Vripple = 9.3V / (50Hz × 1kΩ × 100µF)
Vripple ≈ 1.86V
```

**DC Output Voltage**:
```
Vdc ≈ Vpeak - (Vripple / 2)
Vdc ≈ 9.3V - 0.93V ≈ 8.37V
```

### Diode Model Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| Is | 1e-14 A | Saturation current |
| Rs | 10Ω | Series resistance |
| N | 1.8 | Emission coefficient |

### Simulation Parameters
- **Analysis Type**: Transient Analysis
- **Time Range**: 60 ms (3 cycles at 50Hz)
- **Time Step**: 0.1 ms
- **Expected Results**:
  - Positive half-cycles passed
  - Negative half-cycles blocked
  - Smooth DC with ripple when capacitor included

### Waveform Characteristics
- **Input**: Sinusoidal AC (10V peak, 50Hz)
- **Output (no cap)**: Pulsating DC (half-wave)
- **Output (with cap)**: Smoothed DC with ripple

### File Location
`circuits/rectifier.cir`

### Usage
```bash
ngspice circuits/rectifier.cir
```

---

## General Simulation Guidelines

### Running Simulations

1. **Using ngspice directly**:
```bash
ngspice <circuit_file>.cir
```

2. **Using Python wrapper**:
```python
from src.esim_platform import ESimWrapper

wrapper = ESimWrapper()
success, output = wrapper.simulate_circuit('circuits/<circuit_file>.cir')
print(output)
```

3. **Using eSim GUI**:
- Open eSim application
- Load the .cir file
- Run simulation from the GUI
- View results in the plotter

### Common SPICE Commands

| Command | Purpose |
|---------|---------|
| .op | DC operating point analysis |
| .dc | DC sweep analysis |
| .ac | AC frequency analysis |
| .tran | Transient (time domain) analysis |
| .control/.endc | Control block for commands |
| .print | Output specific variables |
| .plot | Plot results |

### Typical Analysis Workflow

1. **Define Circuit**: Create netlist with components
2. **Set Analysis**: Choose .op, .dc, .ac, or .tran
3. **Run Simulation**: Execute with ngspice
4. **View Results**: Plot or print outputs
5. **Verify**: Compare with theoretical calculations

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Convergence failure | Reduce time step or add small resistors |
| No output | Check .control block and print commands |
| Unexpected results | Verify component values and connections |
| Error messages | Check syntax and component models |

## Design Verification

Each circuit design has been:
- ✅ Theoretically calculated
- ✅ Simulated in eSim/ngspice
- ✅ Results verified against theory
- ✅ Documented with parameters

## References

1. **eSim Documentation**: https://esim.fossee.in/resources
2. **ngspice Manual**: http://ngspice.sourceforge.net/docs.html
3. **SPICE Tutorials**: https://esim.fossee.in/circuit-simulation-project/procedure
4. **Circuit Theory**: Standard electronics textbooks

## Future Circuit Additions

Planned circuits for future releases:
- Full-wave rectifier
- Active filters (Butterworth, Chebyshev)
- Oscillator circuits (Wien bridge, Phase shift)
- Digital logic gates
- Amplifier stages (Common emitter, Common collector)
- Power supply circuits

---

**Last Updated**: February 2026  
**Version**: 1.0.0  
**Author**: eSim Internship Spring 2026

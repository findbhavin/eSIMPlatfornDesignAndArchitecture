import React, { useState, useEffect } from 'react';
import { getCircuits, runSimulation } from '../services/api';
import './SimulationRunner.css';

function SimulationRunner() {
  const [circuits, setCircuits] = useState([]);
  const [selectedCircuit, setSelectedCircuit] = useState('');
  const [loading, setLoading] = useState(false);
  const [simulation, setSimulation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCircuits();
  }, []);

  const fetchCircuits = async () => {
    try {
      const data = await getCircuits();
      if (data.success) {
        setCircuits(data.circuits);
      }
    } catch (err) {
      console.error('Error fetching circuits:', err);
    }
  };

  const handleRunSimulation = async () => {
    if (!selectedCircuit) {
      setError('Please select a circuit');
      return;
    }

    setLoading(true);
    setError(null);
    setSimulation(null);

    try {
      const data = await runSimulation(selectedCircuit);
      if (data.success) {
        setSimulation(data);
      } else {
        setError(data.error || 'Simulation failed');
      }
    } catch (err) {
      setError('Error running simulation: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="simulation-runner">
      <h1>Simulation Runner</h1>
      <p className="subtitle">Execute circuit simulations</p>

      <div className="simulation-controls">
        <div className="control-group">
          <label htmlFor="circuit-select">Select Circuit:</label>
          <select
            id="circuit-select"
            value={selectedCircuit}
            onChange={(e) => setSelectedCircuit(e.target.value)}
            disabled={loading}
          >
            <option value="">-- Choose a circuit --</option>
            {circuits.map((circuit) => (
              <option key={circuit.id} value={circuit.id}>
                {circuit.name}
              </option>
            ))}
          </select>
        </div>

        <button
          className="run-button"
          onClick={handleRunSimulation}
          disabled={!selectedCircuit || loading}
        >
          {loading ? '⏳ Running...' : '▶️ Run Simulation'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {simulation && (
        <div className="simulation-results">
          <h2>Simulation Results</h2>

          <div className="results-header">
            <div className="status-badge" data-status={simulation.status}>
              {simulation.status === 'completed' ? '✓' : '✗'} {simulation.status.toUpperCase()}
            </div>
            <div className="sim-id">ID: {simulation.simulation_id}</div>
          </div>

          {simulation.output && (
            <div className="output-section">
              <h3>Simulation Output</h3>
              <pre className="output-content">{simulation.output}</pre>
            </div>
          )}

          {simulation.error && (
            <div className="error-section">
              <h3>Error Details</h3>
              <pre className="error-content">{simulation.error}</pre>
            </div>
          )}
        </div>
      )}

      <div className="info-box">
        <h3>ℹ️ About Simulation</h3>
        <p>
          This tool runs ngspice simulations on the selected circuit. The simulation
          executes the SPICE netlist and returns the output, which may include:
        </p>
        <ul>
          <li>Operating point analysis results</li>
          <li>DC sweep data</li>
          <li>AC frequency response</li>
          <li>Transient analysis results</li>
        </ul>
        <p className="note">
          <strong>Note:</strong> Simulations are executed on the backend server.
          Ensure ngspice is properly installed and configured.
        </p>
      </div>
    </div>
  );
}

export default SimulationRunner;

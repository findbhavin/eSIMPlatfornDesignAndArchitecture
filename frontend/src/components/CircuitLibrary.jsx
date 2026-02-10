import React, { useState, useEffect } from 'react';
import { getCircuits, getCircuit } from '../services/api';
import './CircuitLibrary.css';

function CircuitLibrary() {
  const [circuits, setCircuits] = useState([]);
  const [selectedCircuit, setSelectedCircuit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [detailsLoading, setDetailsLoading] = useState(false);

  useEffect(() => {
    fetchCircuits();
  }, []);

  const fetchCircuits = async () => {
    try {
      const data = await getCircuits();
      if (data.success) {
        setCircuits(data.circuits);
      }
    } catch (error) {
      console.error('Error fetching circuits:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCircuitClick = async (circuitId) => {
    setDetailsLoading(true);
    try {
      const data = await getCircuit(circuitId);
      if (data.success) {
        setSelectedCircuit(data.circuit);
      }
    } catch (error) {
      console.error('Error fetching circuit details:', error);
    } finally {
      setDetailsLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading circuits...</div>;
  }

  return (
    <div className="circuit-library">
      <h1>Circuit Library</h1>
      <p className="subtitle">Browse available circuit designs</p>

      <div className="library-content">
        <div className="circuits-list">
          <h2>Available Circuits ({circuits.length})</h2>
          {circuits.length === 0 ? (
            <p>No circuits available</p>
          ) : (
            <div className="circuit-cards">
              {circuits.map((circuit) => (
                <div
                  key={circuit.id}
                  className={`circuit-card ${selectedCircuit?.id === circuit.id ? 'active' : ''}`}
                  onClick={() => handleCircuitClick(circuit.id)}
                >
                  <div className="circuit-icon">⚡</div>
                  <h3>{circuit.name}</h3>
                  <p className="circuit-filename">{circuit.filename}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="circuit-details">
          {detailsLoading ? (
            <div className="loading">Loading circuit details...</div>
          ) : selectedCircuit ? (
            <>
              <h2>{selectedCircuit.name}</h2>
              <div className="details-section">
                <h3>Circuit Information</h3>
                <div className="info-grid">
                  <div className="info-item">
                    <strong>Circuit Name:</strong>
                    <span>{selectedCircuit.circuit_name || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <strong>Components:</strong>
                    <span>{selectedCircuit.component_count || 0}</span>
                  </div>
                  <div className="info-item">
                    <strong>Nodes:</strong>
                    <span>{selectedCircuit.node_count || 0}</span>
                  </div>
                </div>
              </div>

              {selectedCircuit.components && selectedCircuit.components.length > 0 && (
                <div className="details-section">
                  <h3>Components</h3>
                  <table className="components-table">
                    <thead>
                      <tr>
                        <th>Type</th>
                        <th>Name</th>
                        <th>Nodes</th>
                        <th>Value</th>
                      </tr>
                    </thead>
                    <tbody>
                      {selectedCircuit.components.map((comp, idx) => (
                        <tr key={idx}>
                          <td>{comp.type}</td>
                          <td>{comp.name}</td>
                          <td>{comp.nodes.join(', ')}</td>
                          <td>{comp.value || '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              {selectedCircuit.netlist && (
                <div className="details-section">
                  <h3>SPICE Netlist</h3>
                  <pre className="netlist-code">{selectedCircuit.netlist}</pre>
                </div>
              )}
            </>
          ) : (
            <div className="no-selection">
              <p>Select a circuit to view details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default CircuitLibrary;

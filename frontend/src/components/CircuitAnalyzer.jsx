import React, { useState } from 'react';
import { analyzeCircuit } from '../services/api';
import './CircuitAnalyzer.css';

function CircuitAnalyzer() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const data = await analyzeCircuit(file);
      if (data.success) {
        setAnalysis(data.analysis);
      } else {
        setError(data.error || 'Analysis failed');
      }
    } catch (err) {
      setError('Error analyzing circuit: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="circuit-analyzer">
      <h1>Circuit Analyzer</h1>
      <p className="subtitle">Upload and analyze SPICE netlist files</p>

      <div className="upload-section">
        <div className="file-input-wrapper">
          <input
            type="file"
            id="netlist-file"
            accept=".cir,.sp,.net,.txt"
            onChange={handleFileChange}
          />
          <label htmlFor="netlist-file" className="file-label">
            {file ? `📄 ${file.name}` : '📁 Choose netlist file'}
          </label>
        </div>
        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={!file || loading}
        >
          {loading ? 'Analyzing...' : 'Analyze Circuit'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {analysis && (
        <div className="analysis-results">
          <h2>Analysis Results</h2>

          <div className="results-grid">
            <div className="result-card">
              <div className="result-icon">📊</div>
              <div className="result-content">
                <h3>{analysis.circuit_name || 'Circuit'}</h3>
                <p>Circuit Name</p>
              </div>
            </div>

            <div className="result-card">
              <div className="result-icon">🔌</div>
              <div className="result-content">
                <h3>{analysis.component_count || 0}</h3>
                <p>Components</p>
              </div>
            </div>

            <div className="result-card">
              <div className="result-icon">⚡</div>
              <div className="result-content">
                <h3>{analysis.node_count || 0}</h3>
                <p>Nodes</p>
              </div>
            </div>
          </div>

          {analysis.components && analysis.components.length > 0 && (
            <div className="components-section">
              <h3>Component Breakdown</h3>
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
                  {analysis.components.map((comp, idx) => (
                    <tr key={idx}>
                      <td>
                        <span className="component-type">{comp.type}</span>
                      </td>
                      <td>{comp.name}</td>
                      <td>{comp.nodes.join(', ')}</td>
                      <td>{comp.value || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {analysis.nodes && analysis.nodes.length > 0 && (
            <div className="nodes-section">
              <h3>Circuit Nodes</h3>
              <div className="nodes-list">
                {analysis.nodes.map((node, idx) => (
                  <span key={idx} className="node-badge">{node}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default CircuitAnalyzer;

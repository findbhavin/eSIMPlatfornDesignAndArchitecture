import React, { useState, useEffect } from 'react';
import { getTools } from '../services/api';
import './ToolManager.css';

function ToolManager() {
  const [tools, setTools] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTools();
  }, []);

  const fetchTools = async () => {
    try {
      const data = await getTools();
      if (data.success) {
        setTools(data.tools);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Error fetching tools: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setLoading(true);
    setError(null);
    fetchTools();
  };

  if (loading) {
    return <div className="loading">Loading tool status...</div>;
  }

  return (
    <div className="tool-manager">
      <h1>Tool Manager</h1>
      <p className="subtitle">Manage simulation tools and dependencies</p>

      <div className="tools-header">
        <button className="refresh-button" onClick={handleRefresh}>
          🔄 Refresh Status
        </button>
      </div>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      <div className="tools-list">
        <h2>Required Tools</h2>

        {Object.entries(tools).map(([toolName, isAvailable]) => (
          <div key={toolName} className="tool-card">
            <div className="tool-info">
              <div className="tool-icon">
                {isAvailable ? '✅' : '❌'}
              </div>
              <div className="tool-details">
                <h3>{toolName}</h3>
                <p className="tool-status">
                  Status: <strong>{isAvailable ? 'Available' : 'Not Found'}</strong>
                </p>
              </div>
            </div>
            {!isAvailable && (
              <div className="tool-actions">
                <button className="install-button" disabled>
                  Install (Manual)
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="installation-guide">
        <h2>Installation Instructions</h2>
        
        <div className="guide-section">
          <h3>🔧 ngspice</h3>
          <p>ngspice is the core simulation engine. Install using:</p>
          <div className="code-block">
            <strong>Ubuntu/Debian:</strong>
            <code>sudo apt-get install ngspice</code>
          </div>
          <div className="code-block">
            <strong>macOS:</strong>
            <code>brew install ngspice</code>
          </div>
          <div className="code-block">
            <strong>Windows:</strong>
            <p>Download from <a href="http://ngspice.sourceforge.net/" target="_blank" rel="noopener noreferrer">
              ngspice.sourceforge.net
            </a></p>
          </div>
        </div>

        <div className="guide-section">
          <h3>🐍 Python 3</h3>
          <p>Python 3.7+ is required for the backend API.</p>
          <div className="code-block">
            <strong>Ubuntu/Debian:</strong>
            <code>sudo apt-get install python3 python3-pip</code>
          </div>
          <div className="code-block">
            <strong>macOS:</strong>
            <code>brew install python3</code>
          </div>
          <div className="code-block">
            <strong>Windows:</strong>
            <p>Download from <a href="https://www.python.org/downloads/" target="_blank" rel="noopener noreferrer">
              python.org
            </a></p>
          </div>
        </div>
      </div>

      <div className="info-box">
        <h3>ℹ️ Tool Information</h3>
        <p>
          These tools are required for circuit simulation and analysis. Make sure they are
          properly installed and accessible from the system PATH.
        </p>
        <ul>
          <li><strong>ngspice:</strong> Open-source circuit simulator based on SPICE</li>
          <li><strong>python3:</strong> Python runtime for backend API and analysis</li>
        </ul>
      </div>
    </div>
  );
}

export default ToolManager;

import React, { useState, useEffect } from 'react';
import { getConfig, updateConfig } from '../services/api';
import './ConfigPanel.css';

function ConfigPanel() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const data = await getConfig();
      if (data.success) {
        setConfig(data.config);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError('Error fetching configuration: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (section, key, value) => {
    setConfig({
      ...config,
      [section]: {
        ...config[section],
        [key]: value,
      },
    });
    setSuccess(false);
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);

    try {
      const data = await updateConfig(config);
      if (data.success) {
        setConfig(data.config);
        setSuccess(true);
      } else {
        setError(data.error || 'Failed to save configuration');
      }
    } catch (err) {
      setError('Error saving configuration: ' + err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading configuration...</div>;
  }

  return (
    <div className="config-panel">
      <h1>Configuration Panel</h1>
      <p className="subtitle">Manage platform settings</p>

      {error && (
        <div className="error-message">
          ❌ {error}
        </div>
      )}

      {success && (
        <div className="success-message">
          ✅ Configuration saved successfully!
        </div>
      )}

      {config && (
        <>
          <div className="config-section">
            <h2>eSim Configuration</h2>
            <div className="config-fields">
              <div className="field-group">
                <label>Installation Path:</label>
                <input
                  type="text"
                  value={config.esim.installation_path}
                  onChange={(e) => handleInputChange('esim', 'installation_path', e.target.value)}
                />
              </div>

              <div className="field-group">
                <label>ngspice Path:</label>
                <input
                  type="text"
                  value={config.esim.ngspice_path}
                  onChange={(e) => handleInputChange('esim', 'ngspice_path', e.target.value)}
                />
              </div>

              <div className="field-group">
                <label>Timeout (seconds):</label>
                <input
                  type="number"
                  value={config.esim.timeout}
                  onChange={(e) => handleInputChange('esim', 'timeout', parseInt(e.target.value))}
                />
              </div>
            </div>
          </div>

          <div className="config-section">
            <h2>Simulation Configuration</h2>
            <div className="config-fields">
              <div className="field-group">
                <label>Output Directory:</label>
                <input
                  type="text"
                  value={config.simulation.output_dir}
                  onChange={(e) => handleInputChange('simulation', 'output_dir', e.target.value)}
                />
              </div>

              <div className="field-group">
                <label>Verbosity:</label>
                <select
                  value={config.simulation.verbosity}
                  onChange={(e) => handleInputChange('simulation', 'verbosity', e.target.value)}
                >
                  <option value="quiet">Quiet</option>
                  <option value="normal">Normal</option>
                  <option value="verbose">Verbose</option>
                </select>
              </div>

              <div className="field-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    checked={config.simulation.keep_intermediate_files}
                    onChange={(e) => handleInputChange('simulation', 'keep_intermediate_files', e.target.checked)}
                  />
                  Keep Intermediate Files
                </label>
              </div>
            </div>
          </div>

          <div className="config-section">
            <h2>Circuit Configuration</h2>
            <div className="config-fields">
              <div className="field-group">
                <label>Default Ground Node:</label>
                <input
                  type="text"
                  value={config.circuit.default_ground}
                  onChange={(e) => handleInputChange('circuit', 'default_ground', e.target.value)}
                />
              </div>

              <div className="field-group">
                <label>Default Temperature (°C):</label>
                <input
                  type="number"
                  value={config.circuit.default_temp}
                  onChange={(e) => handleInputChange('circuit', 'default_temp', parseInt(e.target.value))}
                />
              </div>

              <div className="field-group">
                <label>Default Precision:</label>
                <input
                  type="number"
                  step="0.000001"
                  value={config.circuit.default_precision}
                  onChange={(e) => handleInputChange('circuit', 'default_precision', parseFloat(e.target.value))}
                />
              </div>
            </div>
          </div>

          <div className="actions">
            <button
              className="save-button"
              onClick={handleSave}
              disabled={saving}
            >
              {saving ? 'Saving...' : '💾 Save Configuration'}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ConfigPanel;

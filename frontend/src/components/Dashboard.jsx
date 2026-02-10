import React, { useState, useEffect } from 'react';
import { getCircuits, getTools } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [stats, setStats] = useState({
    totalCircuits: 0,
    toolsAvailable: 0,
    recentSimulations: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [circuitsData, toolsData] = await Promise.all([
          getCircuits(),
          getTools(),
        ]);

        setStats({
          totalCircuits: circuitsData.count || 0,
          toolsAvailable: toolsData.all_available ? 2 : 0,
          recentSimulations: 0,
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>eSim Platform Dashboard</h1>
      <p className="subtitle">Welcome to the eSim Circuit Simulation Platform</p>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3>{stats.totalCircuits}</h3>
            <p>Available Circuits</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔧</div>
          <div className="stat-content">
            <h3>{stats.toolsAvailable}/2</h3>
            <p>Tools Available</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-content">
            <h3>{stats.recentSimulations}</h3>
            <p>Recent Simulations</p>
          </div>
        </div>
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <button className="action-button" onClick={() => window.location.href = '/#/circuits'}>
            <span className="action-icon">📚</span>
            <span>Browse Circuits</span>
          </button>
          <button className="action-button" onClick={() => window.location.href = '/#/analyzer'}>
            <span className="action-icon">🔍</span>
            <span>Analyze Circuit</span>
          </button>
          <button className="action-button" onClick={() => window.location.href = '/#/simulate'}>
            <span className="action-icon">▶️</span>
            <span>Run Simulation</span>
          </button>
          <button className="action-button" onClick={() => window.location.href = '/#/config'}>
            <span className="action-icon">⚙️</span>
            <span>Configuration</span>
          </button>
        </div>
      </div>

      <div className="info-section">
        <h2>About</h2>
        <p>
          The eSim Platform is a comprehensive web interface for circuit simulation
          and analysis. It provides tools for designing, analyzing, and simulating
          electronic circuits using ngspice simulation engine.
        </p>
        <ul>
          <li>✓ Circuit Library with pre-built examples</li>
          <li>✓ Upload and analyze custom SPICE netlists</li>
          <li>✓ Run simulations and view results</li>
          <li>✓ Manage simulation tools and configuration</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;

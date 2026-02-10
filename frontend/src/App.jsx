import React from 'react';
import { HashRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CircuitLibrary from './components/CircuitLibrary';
import CircuitAnalyzer from './components/CircuitAnalyzer';
import SimulationRunner from './components/SimulationRunner';
import ToolManager from './components/ToolManager';
import ConfigPanel from './components/ConfigPanel';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="nav-container">
            <div className="nav-brand">
              <Link to="/">⚡ eSim Platform</Link>
            </div>
            <ul className="nav-links">
              <li><Link to="/">Dashboard</Link></li>
              <li><Link to="/circuits">Circuits</Link></li>
              <li><Link to="/analyzer">Analyzer</Link></li>
              <li><Link to="/simulate">Simulate</Link></li>
              <li><Link to="/tools">Tools</Link></li>
              <li><Link to="/config">Config</Link></li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/circuits" element={<CircuitLibrary />} />
            <Route path="/analyzer" element={<CircuitAnalyzer />} />
            <Route path="/simulate" element={<SimulationRunner />} />
            <Route path="/tools" element={<ToolManager />} />
            <Route path="/config" element={<ConfigPanel />} />
          </Routes>
        </main>

        <footer className="footer">
          <p>eSim Platform © 2026 | eSim Semester Long Internship Spring 2026</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

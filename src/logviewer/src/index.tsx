import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import LogViewer from './LogViewer';
import './LogViewer.css';

const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    // Check localStorage first, then system preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme === 'dark';
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
    document.body.className = darkMode ? 'bg-dark text-light' : 'bg-light text-dark';
    
    // Save to localStorage
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  return (
    <div className={`app-container ${darkMode ? 'theme-dark' : 'theme-light'}`}>
      <header className="app-header">
        <div className="container-fluid d-flex justify-content-between align-items-center">
          <h1 className="mb-0">
            <i className="bi bi-bar-chart-line-fill me-3"></i>
            Semantic Kernel Log Viewer
          </h1>
          <button 
            className="btn btn-outline-light btn-sm"
            onClick={toggleTheme}
            title={`Switch to ${darkMode ? 'light' : 'dark'} mode`}
          >
            <i className={`bi ${darkMode ? 'bi-sun-fill' : 'bi-moon-fill'} me-2`}></i>
            {darkMode ? 'Light' : 'Dark'}
          </button>
        </div>
      </header>
      <main className="app-main">
        <div className="container-fluid h-100">
          <LogViewer darkMode={darkMode} />
        </div>
      </main>
      <footer className="app-footer">
        <div className="container-fluid">
          <p className="mb-0">
            <i className="bi bi-c-circle me-2"></i>
            2025 Semantic Kernel Project - Enterprise Log Analysis Platform
          </p>
        </div>
      </footer>
    </div>
  );
};

ReactDOM.render(<App />, document.getElementById('root'));

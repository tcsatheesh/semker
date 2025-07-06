import React from 'react';
import ReactDOM from 'react-dom';
import LogViewer from './LogViewer';
import './LogViewer.css';

const App: React.FC = () => (
  <div className="app-container">
    <header className="app-header">
      <h1>Semantic Kernel Log Viewer</h1>
    </header>
    <main className="app-main">
      <LogViewer />
    </main>
    <footer className="app-footer">
      <p>© 2025 Semantic Kernel Project</p>
    </footer>
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));

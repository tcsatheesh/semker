import React from 'react';
import ReactDOM from 'react-dom';
import LogViewer from './LogViewer';
import './LogViewer.css';

const App: React.FC = () => (
  <div>
    <h1>Standalone Log Viewer</h1>
    <LogViewer />
  </div>
);

ReactDOM.render(<App />, document.getElementById('root'));

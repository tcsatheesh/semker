import React, { useState, useEffect } from 'react';
import './LogViewer.css';

type LogEntry = {
  [key: string]: any;
};

const LogViewer: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredLogs, setFilteredLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    fetch('/src/backend/httpx.jsonl')
      .then((response) => response.text())
      .then((data) => {
        const parsedLogs = data
          .split('\n')
          .filter((line) => line.trim() !== '')
          .map((line) => JSON.parse(line));
        setLogs(parsedLogs);
        setFilteredLogs(parsedLogs);
      })
      .catch((error) => console.error('Error loading logs:', error));
  }, []);

  useEffect(() => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    setFilteredLogs(
      logs.filter((log) =>
        JSON.stringify(log).toLowerCase().includes(lowerCaseSearchTerm)
      )
    );
  }, [searchTerm, logs]);

  return (
    <div className="log-viewer">
      <input
        type="text"
        placeholder="Search logs..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-bar"
      />
      <div className="log-entries">
        {filteredLogs.map((log, index) => (
          <pre key={index} className="log-entry">
            {JSON.stringify(log, null, 2)}
          </pre>
        ))}
      </div>
    </div>
  );
};

export default LogViewer;
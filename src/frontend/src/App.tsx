import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import MainContent from './components/MainContent';
import Footer from './components/Footer';
import './App.css';

const App: React.FC = () => {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Check localStorage, default to light mode first
    const saved = localStorage.getItem('theme');
    if (saved) {
      return saved === 'dark';
    }
    // Default to light mode instead of system preference
    return false;
  });

  useEffect(() => {
    // Apply theme to document
    const theme = isDarkMode ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    console.log('Theme applied:', theme, 'to', document.documentElement);
  }, [isDarkMode]);

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className="app">
      <Header isDarkMode={isDarkMode} onToggleTheme={toggleTheme} />
      <MainContent />
      <Footer />
    </div>
  );
};

export default App;

import React from 'react';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; {currentYear} Semker. All rights reserved.</p>
        <p>Built with React & TypeScript | Backend integration ready</p>
      </div>
    </footer>
  );
};

export default Footer;

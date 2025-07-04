import React, { useState, useEffect } from 'react';
import { apiService } from '../services/apiService';

interface Message {
  id: string;
  content: string;
  timestamp: string;
  status: string;
}

const MainContent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [sender, setSender] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getMessages();
      setMessages(data);
    } catch (err) {
      setError('Failed to load messages');
      console.error('Error loading messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setSuccess(null);
      
      const message = await apiService.createMessage(newMessage, sender || 'anonymous');
      setMessages(prev => [message, ...prev]);
      setNewMessage('');
      setSuccess('Message sent successfully!');
    } catch (err) {
      setError('Failed to send message');
      console.error('Error sending message:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleHealthCheck = async () => {
    try {
      setLoading(true);
      setError(null);
      const health = await apiService.healthCheck();
      setSuccess(`Backend is healthy: ${health.status}`);
    } catch (err) {
      setError('Backend health check failed');
      console.error('Health check error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="main-content">
      <div className="container">
        <h1>Semker Message Hub</h1>
        
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        
        <div className="card">
          <h2>Backend Integration</h2>
          <button 
            onClick={handleHealthCheck} 
            disabled={loading}
            className="button"
          >
            {loading ? 'Checking...' : 'Check Backend Health'}
          </button>
        </div>

        <div className="card">
          <h2>Send Message</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="sender" className="form-label">
                Sender (optional):
              </label>
              <input
                type="text"
                id="sender"
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                className="form-input"
                placeholder="Your name or ID (defaults to 'anonymous')"
                disabled={loading}
              />
            </div>
            <div className="form-group">
              <label htmlFor="message" className="form-label">
                Message Content:
              </label>
              <textarea
                id="message"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className="form-textarea"
                placeholder="Enter your message here..."
                disabled={loading}
              />
            </div>
            <button 
              type="submit" 
              disabled={loading || !newMessage.trim()}
              className="button"
            >
              {loading ? 'Sending...' : 'Send Message'}
            </button>
          </form>
        </div>

        <div className="card">
          <h2>Messages</h2>
          {loading && messages.length === 0 ? (
            <div className="loading">Loading messages...</div>
          ) : (
            <>
              <button 
                onClick={loadMessages} 
                disabled={loading}
                className="button"
                style={{ marginBottom: '1rem' }}
              >
                {loading ? 'Refreshing...' : 'Refresh Messages'}
              </button>
              
              {messages.length === 0 ? (
                <p>No messages yet. Send your first message!</p>
              ) : (
                <div>
                  {messages.map((message) => (
                    <div key={message.id} className="card" style={{ marginLeft: '1rem' }}>
                      <p><strong>ID:</strong> {message.id}</p>
                      <p><strong>Content:</strong> {message.content}</p>
                      <p><strong>Status:</strong> {message.status}</p>
                      <p><strong>Timestamp:</strong> {new Date(message.timestamp).toLocaleString()}</p>
                    </div>
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
};

export default MainContent;

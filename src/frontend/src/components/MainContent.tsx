import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { apiService } from '../services/apiService';

interface Message {
  id: string;
  message: string;
  timestamp: string;
  status: string;
}

interface ChatMessage {
  id: string;
  text: string;
  timestamp: Date;
  isUser: boolean;
  status?: string;
  isLoading?: boolean;
  duration?: number; // Duration in milliseconds
  isIntermediate?: boolean; // For polling responses that will disappear
  isCompleted?: boolean; // For intermediate messages that are now completed
  messageId?: string; // Backend message ID for tracking
}

const MainContent: React.FC = () => {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activePolling, setActivePolling] = useState<Set<string>>(new Set());
  const chatEndRef = useRef<HTMLDivElement>(null);
  const pollingIntervals = useRef<Map<string, NodeJS.Timeout>>(new Map());

  useEffect(() => {
    checkConnection();
    loadInitialMessages();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [chatMessages]);

  // Cleanup polling intervals on unmount
  useEffect(() => {
    const intervals = pollingIntervals.current;
    return () => {
      intervals.forEach((interval) => {
        clearInterval(interval);
      });
      intervals.clear();
    };
  }, []);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkConnection = async () => {
    try {
      await apiService.healthCheck();
      setIsConnected(true);
      setError(null);
    } catch (err) {
      setIsConnected(false);
      setError('Cannot connect to server');
    }
  };

  const loadInitialMessages = async () => {
    try {
      const messages = await apiService.getMessages();
      const chatMsgs: ChatMessage[] = messages.map((msg: Message) => ({
        id: msg.id,
        text: msg.message,
        timestamp: new Date(msg.timestamp),
        isUser: false,
        status: msg.status
      }));
      setChatMessages(chatMsgs);
    } catch (err) {
      console.error('Error loading messages:', err);
    }
  };

  const formatDuration = (milliseconds: number): string => {
    if (milliseconds < 1000) {
      return `${milliseconds}ms`;
    }
    return `${(milliseconds / 1000).toFixed(1)}s`;
  };

  const removeIntermediateMessages = (messageId: string) => {
    // Don't remove intermediate messages - instead mark them as completed
    setChatMessages(prev => prev.map(msg => 
      (msg.isIntermediate && msg.messageId === messageId) 
        ? { ...msg, isIntermediate: false, isCompleted: true }
        : msg
    ));
  };

  const startPolling = async (messageId: string, startTime: number) => {
    if (activePolling.has(messageId)) return;

    setActivePolling(prev => new Set(prev).add(messageId));

    const poll = async () => {
      try {
        const updates = await apiService.getMessageUpdates(messageId);
        const currentTime = Date.now();
        const duration = currentTime - startTime;

        if (updates && updates.length > 0) {
          const latestUpdate = updates[updates.length - 1];
          
          // Create appropriate message text based on status
          let messageText = '';
          if (latestUpdate.status === 'received') {
            messageText = `✅ Message received and queued for processing...`;
          } else if (latestUpdate.status === 'processing') {
            messageText = `⚡ Processing your message...`;
          } else {
            messageText = `Processing... Status: ${latestUpdate.status}`;
          }
          
          // Add intermediate status message
          const intermediateMessage: ChatMessage = {
            id: `intermediate-${messageId}-${Date.now()}`,
            text: messageText,
            timestamp: new Date(),
            isUser: false,
            status: latestUpdate.status,
            duration,
            isIntermediate: true,
            messageId
          };

          setChatMessages(prev => {
            // Don't remove previous intermediate messages, just add this one
            // Remove only the previous intermediate message with the same exact ID pattern
            const filtered = prev.filter(msg => 
              !(msg.isIntermediate && msg.messageId === messageId && msg.id.startsWith(`intermediate-${messageId}`))
            );
            return [...filtered, intermediateMessage];
          });

          // If processing is complete, show final message and mark intermediate messages as completed
          if (latestUpdate.status === 'processed') {
            setTimeout(() => {
              // Mark intermediate messages as completed instead of removing them
              removeIntermediateMessages(messageId);
              
              const finalMessage: ChatMessage = {
                id: `final-${messageId}`,
                text: `✅ ${latestUpdate.result || ''}`,
                timestamp: new Date(latestUpdate.processed_at),
                isUser: false,
                status: 'processed',
                duration,
                messageId
              };

              setChatMessages(prev => [...prev, finalMessage]);
            }, 500); // Small delay to show the intermediate message briefly

            // Stop polling
            const interval = pollingIntervals.current.get(messageId);
            if (interval) {
              clearInterval(interval);
              pollingIntervals.current.delete(messageId);
            }
            setActivePolling(prev => {
              const newSet = new Set(prev);
              newSet.delete(messageId);
              return newSet;
            });
          }
        }
      } catch (err) {
        console.error('Error polling for updates:', err);
        // Stop polling on error
        const interval = pollingIntervals.current.get(messageId);
        if (interval) {
          clearInterval(interval);
          pollingIntervals.current.delete(messageId);
        }
        setActivePolling(prev => {
          const newSet = new Set(prev);
          newSet.delete(messageId);
          return newSet;
        });
      }
    };

    // Start polling every 1 second
    const interval = setInterval(poll, 1000);
    pollingIntervals.current.set(messageId, interval);

    // Initial poll
    poll();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !isConnected) return;

    const startTime = Date.now();
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      text: newMessage.trim(),
      timestamp: new Date(),
      isUser: true
    };

    // Add user message immediately
    setChatMessages(prev => [...prev, userMessage]);
    
    // Add loading message for server response
    const loadingMessage: ChatMessage = {
      id: `loading-${Date.now()}`,
      text: 'Sending...',
      timestamp: new Date(),
      isUser: false,
      isLoading: true
    };
    setChatMessages(prev => [...prev, loadingMessage]);
    
    setNewMessage('');
    setError(null);

    try {
      // Send message to server and track duration
      const response = await apiService.createMessage(userMessage.text);
      const requestDuration = Date.now() - startTime;
      
      // Remove loading message
      setChatMessages(prev => prev.filter(msg => !msg.isLoading));

      // Show initial "received" status as an intermediate message
      const receivedMessage: ChatMessage = {
        id: `intermediate-${response.id}-received`,
        text: `✅ Message received and queued for processing... (${formatDuration(requestDuration)})`,
        timestamp: new Date(response.timestamp),
        isUser: false,
        status: response.status,
        duration: requestDuration,
        isIntermediate: true,
        messageId: response.id
      };

      setChatMessages(prev => [...prev, receivedMessage]);

      // Start polling for processing updates
      startPolling(response.id, startTime);

    } catch (err) {
      // Remove loading message and show error
      setChatMessages(prev => prev.filter(msg => !msg.isLoading));
      const errorDuration = Date.now() - startTime;
      setError(`Failed to send message (${formatDuration(errorDuration)})`);
      console.error('Error sending message:', err);
    }
  };

  return (
    <main className="main-content">
      <div className="container">
        <div className="chat-container">
          <div className="chat-header">
            <h1>Semantic Kernel Agentic AI Chat</h1>
            <div className="connection-status">
              <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                ●
              </span>
              <span className="status-text">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
              <button 
                onClick={checkConnection}
                className="button small"
                style={{ marginLeft: '1rem' }}
              >
                Reconnect
              </button>
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <div className="chat-messages">
            {chatMessages.length === 0 ? (
              <div className="empty-chat">
                <p>Welcome to Semker Chat! Send a message to get started.</p>
              </div>
            ) : (
              chatMessages.map((message) => (
                <div 
                  key={message.id} 
                  className={`chat-message ${message.isUser ? 'user' : 'server'} ${message.isLoading ? 'loading' : ''} ${message.isIntermediate ? 'intermediate' : ''} ${message.isCompleted ? 'completed' : ''}`}
                >
                  <div className="message-content">
                    <div className="message-text">
                      {message.isLoading ? (
                        <div className="typing-indicator">
                          <span></span>
                          <span></span>
                          <span></span>
                        </div>
                      ) : message.isUser ? (
                        message.text
                      ) : (
                        <ReactMarkdown>{message.text}</ReactMarkdown>
                      )}
                    </div>
                    <div className="message-meta">
                      <span className="message-time">
                        {message.timestamp.toLocaleTimeString()}
                      </span>
                      {message.duration && (
                        <span className="message-duration">
                          {formatDuration(message.duration)}
                        </span>
                      )}
                      {message.status && (
                        <span className={`message-status status-${message.status}`}>
                          {message.status}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="chat-input">
            <form onSubmit={handleSubmit} className="chat-form">
              <div className="input-group">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder={isConnected ? "Type your message..." : "Connect to server first"}
                  disabled={!isConnected}
                  className="chat-input-field"
                  autoFocus
                />
                <button 
                  type="submit" 
                  disabled={!isConnected || !newMessage.trim()}
                  className="button send-button"
                >
                  Send
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
};

export default MainContent;

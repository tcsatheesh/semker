import React, { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { apiService, getConversationId, generateNewConversationId } from '../services/apiService';

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
  agentName?: string; // Name of the agent that processed the message
}

const MainContent: React.FC = () => {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activePolling, setActivePolling] = useState<Set<string>>(new Set());
  const [conversationId, setConversationId] = useState<string>(getConversationId());
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
      
      // Filter out any messages with empty text to prevent empty completed messages
      const validMessages = chatMsgs.filter(msg => msg.text && msg.text.trim());
      setChatMessages(validMessages);
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

  const startPolling = async (messageId: string, startTime: number) => {
    if (activePolling.has(messageId)) return;

    setActivePolling(prev => new Set(prev).add(messageId));
    let lastStatus = '';
    let lastResult = '';

    const poll = async () => {
      try {
        const updates = await apiService.getMessageUpdates(messageId);
        const currentTime = Date.now();
        const duration = currentTime - startTime;

        if (updates && updates.length > 0) {
          const latestUpdate = updates[updates.length - 1];
          
          // Check if status or result has changed from the last poll
          const statusChanged = latestUpdate.status !== lastStatus;
          const resultChanged = latestUpdate.result !== lastResult;
          
          if (statusChanged || resultChanged) {
            // Update our tracking variables
            lastStatus = latestUpdate.status;
            lastResult = latestUpdate.result;
            
            // Only add intermediate message if not in a completion state
            // Completion states will be handled by the final message logic below
            if (latestUpdate.status !== 'completed' && latestUpdate.status !== 'failed') {
              // Only create intermediate message if there's actual result content
              if (latestUpdate.result && latestUpdate.result.trim()) {
                // Create appropriate message text based on status
                let messageText = '';
                if (latestUpdate.status === 'received') {
                  messageText = `✅ ${latestUpdate.result}`;
                } else if (latestUpdate.status === 'inprogress') {
                  messageText = `⚡ ${latestUpdate.result}`;
                } else {
                  messageText = `${latestUpdate.result}`;
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
                  messageId,
                  agentName: latestUpdate.agent_name
                };

                setChatMessages(prev => {
                  // Check if we already have this exact intermediate message content
                  const hasSameContent = prev.some(msg => 
                    msg.isIntermediate && 
                    msg.messageId === messageId && 
                    msg.text === messageText
                  );
                  
                  // Only add if we don't already have the same content
                  if (!hasSameContent) {
                    return [...prev, intermediateMessage];
                  }
                  
                  // If same content exists, just update the duration of the most recent one
                  return prev.map(msg => {
                    if (msg.isIntermediate && msg.messageId === messageId && msg.text === messageText) {
                      const intermediateMessages = prev.filter(m => 
                        m.isIntermediate && m.messageId === messageId && m.text === messageText
                      );
                      const mostRecent = intermediateMessages[intermediateMessages.length - 1];
                      if (msg.id === mostRecent.id) {
                        return { ...msg, duration };
                      }
                    }
                    return msg;
                  });
                });
              }
            }
          } else {
            // Only duration has changed, update the most recent intermediate message for this messageId
            setChatMessages(prev => prev.map(msg => {
              if (msg.isIntermediate && msg.messageId === messageId) {
                // Find the most recent intermediate message and update its duration
                const intermediateMessages = prev.filter(m => m.isIntermediate && m.messageId === messageId);
                if (intermediateMessages.length > 0) {
                  const mostRecent = intermediateMessages[intermediateMessages.length - 1];
                  if (msg.id === mostRecent.id) {
                    return { ...msg, duration };
                  }
                }
              }
              return msg;
            }));
          }

          // If processing is complete, show final message and mark intermediate messages as completed
          if (latestUpdate.status === 'completed' || latestUpdate.status === 'failed') {
            setTimeout(() => {
              setChatMessages(prev => {
                // Check if we already have a final message for this messageId
                const hasFinalMessage = prev.some(msg => 
                  msg.messageId === messageId && 
                  !msg.isIntermediate && 
                  !msg.isCompleted &&
                  msg.id.startsWith('final-')
                );
                
                // Mark intermediate messages as completed
                const updatedMessages = prev.map(msg => 
                  (msg.isIntermediate && msg.messageId === messageId) 
                    ? { ...msg, isIntermediate: false, isCompleted: true }
                    : msg
                );
                
                // Only create final message if there's actual result content and no final message exists
                if (latestUpdate.result && latestUpdate.result.trim() && !hasFinalMessage) {
                  const finalMessage: ChatMessage = {
                    id: `final-${messageId}`,
                    text: `✅ ${latestUpdate.result}`,
                    timestamp: new Date(latestUpdate.processed_at),
                    isUser: false,
                    status: `${latestUpdate.status || ''}`,
                    duration,
                    messageId,
                    agentName: latestUpdate.agent_name
                  };
                  
                  return [...updatedMessages, finalMessage];
                }
                
                return updatedMessages;
              });
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

  const startNewConversation = () => {
    // Generate new conversation ID
    const newId = generateNewConversationId();
    setConversationId(newId);
    
    // Clear chat messages
    setChatMessages([]);
    
    // Clear any active polling
    pollingIntervals.current.forEach((interval) => {
      clearInterval(interval);
    });
    pollingIntervals.current.clear();
    setActivePolling(new Set());
    
    // Clear any errors
    setError(null);
    
    console.log('Started new conversation with ID:', newId);
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
      
      // Remove loading message
      setChatMessages(prev => prev.filter(msg => !msg.isLoading));

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
            <div className="header-main">
              <h1>Semantic Kernel Agentic AI Chat</h1>
              <div className="conversation-info">
                <small>Conversation ID: {conversationId}</small>
              </div>
            </div>
            <div className="header-controls">
              <div className="connection-status">
                <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                  ●
                </span>
                <span className="status-text">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <button 
                onClick={checkConnection}
                className="button small"
                style={{ marginLeft: '1rem' }}
              >
                Reconnect
              </button>
              <button 
                onClick={startNewConversation}
                className="button small"
                style={{ marginLeft: '0.5rem' }}
              >
                New Chat
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
                        <ReactMarkdown 
                          remarkPlugins={[remarkGfm]}
                          components={{
                            table: ({node, ...props}) => (
                              <table className="markdown-table" {...props} />
                            ),
                            th: ({node, ...props}) => (
                              <th className="markdown-th" {...props} />
                            ),
                            td: ({node, ...props}) => (
                              <td className="markdown-td" {...props} />
                            ),
                            tr: ({node, ...props}) => (
                              <tr className="markdown-tr" {...props} />
                            ),
                            thead: ({node, ...props}) => (
                              <thead className="markdown-thead" {...props} />
                            ),
                            tbody: ({node, ...props}) => (
                              <tbody className="markdown-tbody" {...props} />
                            )
                          }}
                        >
                          {message.text}
                        </ReactMarkdown>
                      )}
                    </div>
                    <div className="message-meta">
                      <span className="message-time">
                        {message.timestamp.toLocaleTimeString()}
                      </span>
                      {message.agentName && (
                        <span className="message-agent">
                          {message.agentName}
                        </span>
                      )}
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

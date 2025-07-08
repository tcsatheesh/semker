import React, { useState, useEffect } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, vs } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './LogViewer.css';

type LogEntry = {
  [key: string]: any;
};

interface ConversationGroup {
  conversationId: string;
  messages: LogEntry[];
  isExpanded: boolean;
}

interface LogViewerProps {
  darkMode: boolean;
}

const LogViewer: React.FC<LogViewerProps> = ({ darkMode }) => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [conversationGroups, setConversationGroups] = useState<ConversationGroup[]>([]);
  const [selectedLog, setSelectedLog] = useState<LogEntry | null>(null);

  // Extract conversation ID from log entry
  const extractConversationId = (log: LogEntry): string | null => {
    try {
      // Check if this is our expected log structure
      if (log.message && log.message.Request && log.message.Request.Headers) {
        const headers = log.message.Request.Headers;
        // Look for conversation ID in various possible header formats
        return headers['x-ms-conversation-id'] || 
               headers['X-Ms-Conversation-Id'] || 
               headers['X-MS-CONVERSATION-ID'] ||
               null;
      }
    } catch (error) {
      console.error('Error extracting conversation ID:', error);
    }
    return null;
  };

  // Group logs by conversation ID
  const groupLogsByConversation = (logs: LogEntry[]): ConversationGroup[] => {
    const grouped = new Map<string, LogEntry[]>();
    const ungrouped: LogEntry[] = [];

    logs.forEach(log => {
      const conversationId = extractConversationId(log);
      if (conversationId) {
        if (!grouped.has(conversationId)) {
          grouped.set(conversationId, []);
        }
        grouped.get(conversationId)!.push(log);
      } else {
        ungrouped.push(log);
      }
    });

    const groups: ConversationGroup[] = [];
    
    // Add grouped conversations
    grouped.forEach((messages, conversationId) => {
      groups.push({
        conversationId,
        messages: messages.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()),
        isExpanded: true // Default to expanded so we can see the content immediately
      });
    });

    // Add ungrouped messages as individual groups
    ungrouped.forEach((log, index) => {
      groups.push({
        conversationId: `ungrouped-${index}`,
        messages: [log],
        isExpanded: true // Default to expanded
      });
    });

    return groups.sort((a, b) => {
      // Sort by timestamp of first message in each group
      const aTime = a.messages[0]?.timestamp ? new Date(a.messages[0].timestamp).getTime() : 0;
      const bTime = b.messages[0]?.timestamp ? new Date(b.messages[0].timestamp).getTime() : 0;
      return bTime - aTime; // Most recent first
    });
  };

  const toggleConversation = (conversationId: string) => {
    setConversationGroups(prev => 
      prev.map(group => 
        group.conversationId === conversationId 
          ? { ...group, isExpanded: !group.isExpanded }
          : group
      )
    );
  };

  useEffect(() => {
    fetch('/logs')
      .then((response) => response.json())
      .then((data) => {
        setLogs(data);
        setConversationGroups(groupLogsByConversation(data));
      })
      .catch((error) => console.error('Error loading logs:', error));
  }, []);

  useEffect(() => {
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    const filtered = logs.filter((log) =>
      JSON.stringify(log).toLowerCase().includes(lowerCaseSearchTerm)
    );
    setConversationGroups(groupLogsByConversation(filtered));
  }, [searchTerm, logs]);

  const handleLogClick = (log: LogEntry) => {
    setSelectedLog(log);
  };

  // Filter sensitive headers from request before display
  const sanitizeRequest = (request: any) => {
    if (!request) return {};
    
    const sanitized = { ...request };
    
    // Remove authorization headers (case-insensitive)
    if (sanitized.Headers) {
      const filteredHeaders = { ...sanitized.Headers };
      Object.keys(filteredHeaders).forEach(key => {
        if (key.toLowerCase().includes('authorization') || 
            key.toLowerCase().includes('auth') ||
            key.toLowerCase() === 'x-api-key' ||
            key.toLowerCase() === 'api-key') {
          filteredHeaders[key] = '[REDACTED]';
        }
      });
      sanitized.Headers = filteredHeaders;
    }
    
    return sanitized;
  };

  return (
    <div className={`log-viewer ${darkMode ? 'theme-dark' : 'theme-light'}`}>
      <div className="log-controls">
        <div className="input-group">
          <span className="input-group-text">
            <i className="bi bi-search"></i>
          </span>
          <input
            type="text"
            placeholder="Search logs by conversation ID, method, status..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-control search-bar"
          />
        </div>
      </div>

      <div className="log-layout">
        {/* Left Column - Conversation Tree */}
        <div className="conversation-panel card">
          <div className="card-header">
            <h3 className="mb-0">
              <i className="bi bi-diagram-3-fill me-2"></i>
              Conversations
            </h3>
          </div>
          <div className="card-body p-0">
            <div className="conversation-tree">
              {conversationGroups.map((group) => (
                <div key={group.conversationId} className="conversation-group">
                  <div 
                    className="conversation-header"
                    onClick={() => toggleConversation(group.conversationId)}
                  >
                    <span className={`expand-icon ${group.isExpanded ? 'expanded' : ''}`}>
                      <i className={`bi ${group.isExpanded ? 'bi-chevron-down' : 'bi-chevron-right'}`}></i>
                    </span>
                    <span className="conversation-id">
                      <i className="bi bi-chat-dots me-2"></i>
                      {group.conversationId.startsWith('ungrouped-') 
                        ? 'No Conversation ID' 
                        : group.conversationId.substring(0, 8) + '...'}
                    </span>
                    <span className="message-count badge">
                      {group.messages.length}
                    </span>
                  </div>
                  
                  {group.isExpanded && (
                    <div className="conversation-messages">
                      {group.messages.map((log, index) => (
                        <div 
                          key={`${group.conversationId}-${index}`} 
                          className={`log-entry-tree ${selectedLog === log ? 'selected' : ''}`}
                          onClick={() => handleLogClick(log)}
                        >
                          <div className="log-timestamp">
                            <i className="bi bi-clock me-1"></i>
                            {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'No time'}
                          </div>
                          <div className="log-summary">
                            <i className="bi bi-arrow-left-right me-1"></i>
                            {log.message?.Request?.Method || 'Unknown'} - {log.message?.Response?.['Status Code'] || 'No response'}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column - Request/Response Details */}
        <div className="details-panel">
          {selectedLog ? (
            <>
              <div className="request-panel card">
                <div className="card-header">
                  <h3 className="mb-0">
                    <i className="bi bi-arrow-up-circle-fill me-2"></i>
                    Request
                  </h3>
                </div>
                <div className="card-body p-0">
                  <div className="details-content">
                    <SyntaxHighlighter
                      language="json"
                      style={darkMode ? vscDarkPlus : vs}
                      customStyle={{
                        margin: 0,
                        padding: '1.5rem',
                        background: 'var(--bg-primary)',
                        borderRadius: '8px',
                        border: '1px solid var(--border-color)',
                        fontSize: '0.9rem',
                        lineHeight: '1.4',
                        maxWidth: '100%',
                        overflowX: 'auto',
                        whiteSpace: 'pre-wrap',
                        wordWrap: 'break-word',
                        wordBreak: 'break-word'
                      }}
                      wrapLongLines={true}
                      wrapLines={true}
                      lineProps={{
                        style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' }
                      }}
                    >
                      {JSON.stringify(sanitizeRequest(selectedLog.message?.Request) || {}, null, 2)}
                    </SyntaxHighlighter>
                  </div>
                </div>
              </div>
              
              <div className="response-panel card">
                <div className="card-header">
                  <h3 className="mb-0">
                    <i className="bi bi-arrow-down-circle-fill me-2"></i>
                    Response
                  </h3>
                </div>
                <div className="card-body p-0">
                  <div className="details-content">
                    <SyntaxHighlighter
                      language="json"
                      style={darkMode ? vscDarkPlus : vs}
                      customStyle={{
                        margin: 0,
                        padding: '1.5rem',
                        background: 'var(--bg-primary)',
                        borderRadius: '8px',
                        border: '1px solid var(--border-color)',
                        fontSize: '0.9rem',
                        lineHeight: '1.4',
                        maxWidth: '100%',
                        overflowX: 'auto',
                        whiteSpace: 'pre-wrap',
                        wordWrap: 'break-word',
                        wordBreak: 'break-word'
                      }}
                      wrapLongLines={true}
                      wrapLines={true}
                      lineProps={{
                        style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' }
                      }}
                    >
                      {JSON.stringify(selectedLog.message?.Response || {}, null, 2)}
                    </SyntaxHighlighter>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="no-selection">
              <div className="text-center">
                <i className="bi bi-cursor-fill display-4 mb-3 text-muted"></i>
                <p className="mb-0">Select a log entry to view request and response details</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LogViewer;
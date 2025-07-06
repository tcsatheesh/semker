import React, { useState, useEffect } from 'react';
import './LogViewer.css';

type LogEntry = {
  [key: string]: any;
};

interface ConversationGroup {
  conversationId: string;
  messages: LogEntry[];
  isExpanded: boolean;
}

const LogViewer: React.FC = () => {
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

  return (
    <div className="log-viewer">
      <div className="log-controls">
        <input
          type="text"
          placeholder="Search logs..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-bar"
        />
      </div>

      <div className="log-layout">
        {/* Left Column - Conversation Tree */}
        <div className="conversation-panel">
          <h3>Conversations</h3>
          <div className="conversation-tree">
            {conversationGroups.map((group) => (
              <div key={group.conversationId} className="conversation-group">
                <div 
                  className="conversation-header"
                  onClick={() => toggleConversation(group.conversationId)}
                >
                  <span className={`expand-icon ${group.isExpanded ? 'expanded' : ''}`}>
                    ▶
                  </span>
                  <span className="conversation-id">
                    {group.conversationId.startsWith('ungrouped-') 
                      ? 'No Conversation ID' 
                      : group.conversationId.substring(0, 8) + '...'}
                  </span>
                  <span className="message-count">
                    ({group.messages.length})
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
                          {log.timestamp ? new Date(log.timestamp).toLocaleTimeString() : 'No time'}
                        </div>
                        <div className="log-summary">
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

        {/* Right Column - Request/Response Details */}
        <div className="details-panel">
          {selectedLog ? (
            <>
              <div className="request-panel">
                <h3>Request</h3>
                <div className="details-content">
                  <pre className="json-content">
                    {JSON.stringify(selectedLog.message?.Request || {}, null, 2)}
                  </pre>
                </div>
              </div>
              
              <div className="response-panel">
                <h3>Response</h3>
                <div className="details-content">
                  <pre className="json-content">
                    {JSON.stringify(selectedLog.message?.Response || {}, null, 2)}
                  </pre>
                </div>
              </div>
            </>
          ) : (
            <div className="no-selection">
              <p>Select a log entry to view request and response details</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default LogViewer;
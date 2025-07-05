import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Utility function to generate UUID v4
const generateUUID = (): string => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
};

// Generate and store conversation ID for this session
let conversationId: string = generateUUID();

// Function to get current conversation ID
export const getConversationId = (): string => conversationId;

// Function to generate a new conversation ID (for new chats)
export const generateNewConversationId = (): string => {
  conversationId = generateUUID();
  return conversationId;
};

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to handle common configurations
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle common responses
api.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status);
    return response;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Types for API responses
interface HealthResponse {
  status: string;
  timestamp: string;
  version?: string;
}

interface Message {
  id: string;
  message: string;
  timestamp: string;
  status: string;
}

interface CreateMessageRequest {
  message: string;
}

interface CreateMessageResponse {
  message_id: string;
  status: string;
  received_at: string;
}

// API service methods
export const apiService = {
  // Health check endpoint
  async healthCheck(): Promise<HealthResponse> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Health check failed');
    }
  },

  // Get root endpoint
  async getRoot(): Promise<any> {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch root endpoint');
    }
  },

  // Create a new message
  async createMessage(message: string): Promise<Message> {
    try {
      const payload: CreateMessageRequest = { message };
      const response = await api.post<CreateMessageResponse>('/messages', payload, {
        headers: {
          'x-ms-conversation-id': conversationId
        }
      });
      
      // Transform the response to match our Message interface
      return {
        id: response.data.message_id,
        message: message, // Return the message we sent
        timestamp: response.data.received_at,
        status: response.data.status
      };
    } catch (error) {
      throw new Error('Failed to create message');
    }
  },

  // Get all messages
  async getMessages(): Promise<Message[]> {
    try {
      const response = await api.get('/messages');
      const data = response.data;
      
      // Backend returns { total_messages: number, messages: [] }
      if (data && Array.isArray(data.messages)) {
        return data.messages.map((msg: any) => ({
          id: msg.message_id || msg.id,
          message: msg.message,
          timestamp: msg.received_at || msg.timestamp,
          status: msg.status
        }));
      }
      
      return [];
    } catch (error) {
      console.warn('Messages endpoint error:', error);
      return [];
    }
  },

  // Get message by ID (if backend supports it)
  async getMessageById(id: string): Promise<Message> {
    try {
      const response = await api.get(`/messages/${id}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch message with id: ${id}`);
    }
  },

  // Get message updates/status for polling
  async getMessageUpdates(messageId: string): Promise<any[]> {
    try {
      const response = await api.get(`/messages/${messageId}/updates`);
      // Backend returns the updates array directly, not wrapped in { updates: [] }
      return Array.isArray(response.data) ? response.data : [];
    } catch (error) {
      console.warn(`Updates endpoint error for message ${messageId}:`, error);
      return [];
    }
  },

  // Test endpoint to verify backend connectivity
  async testConnection(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch (error) {
      return false;
    }
  }
};

export default apiService;

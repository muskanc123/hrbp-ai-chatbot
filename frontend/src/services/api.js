/**
 * API Service Layer
 * Handles all HTTP requests to the backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
api.interceptors.request.use(
    (config) => {
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
api.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

export const apiService = {
    // Health check
    healthCheck: async () => {
        const response = await api.get('/health');
        return response.data;
    },

    // Chat
    sendMessage: async (conversationId, message) => {
        const response = await api.post('/api/v1/chat', {
            conversation_id: conversationId,
            message: message,
        });
        return response.data;
    },

    // Conversations
    getConversations: async () => {
        const response = await api.get('/api/v1/conversations');
        return response.data;
    },

    getConversation: async (conversationId) => {
        const response = await api.get(`/api/v1/conversations/${conversationId}`);
        return response.data;
    },

    createConversation: async (title) => {
        const response = await api.post('/api/v1/conversations', { title });
        return response.data;
    },

    deleteConversation: async (conversationId) => {
        const response = await api.delete(`/api/v1/conversations/${conversationId}`);
        return response.data;
    },
};

export default apiService;

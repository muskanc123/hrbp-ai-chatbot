import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatContainer from './components/ChatContainer';
import MessageInput from './components/MessageInput';
import { apiService } from './services/api';

function App() {
    const [conversations, setConversations] = useState([]);
    const [activeConversationId, setActiveConversationId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [loading, setLoading] = useState(false);

    // Load conversations on mount
    useEffect(() => {
        loadConversations();
    }, []);

    // Load messages when conversation changes
    useEffect(() => {
        if (activeConversationId) {
            loadConversation(activeConversationId);
        } else {
            setMessages([]);
        }
    }, [activeConversationId]);

    const loadConversations = async () => {
        try {
            const data = await apiService.getConversations();
            setConversations(data);
        } catch (error) {
            console.error('Error loading conversations:', error);
        }
    };

    const loadConversation = async (conversationId) => {
        try {
            const data = await apiService.getConversation(conversationId);
            setMessages(data.messages || []);
        } catch (error) {
            console.error('Error loading conversation:', error);
        }
    };

    const handleSendMessage = async () => {
        if (!inputValue.trim() || loading) return;

        const userMessage = inputValue;
        setInputValue('');
        setLoading(true);

        // Optimistically add user message to UI immediately
        const tempUserMessage = {
            id: `temp-${Date.now()}`,
            role: 'user',
            content: userMessage,
            created_at: new Date().toISOString()
        };
        setMessages((prev) => [...prev, tempUserMessage]);

        try {
            const response = await apiService.sendMessage(activeConversationId, userMessage);

            // Replace temp message with real messages from server
            setMessages((prev) => [
                ...prev.filter(msg => msg.id !== tempUserMessage.id),
                response.user_message,
                response.assistant_message,
            ]);

            // Update active conversation ID if it was a new conversation
            if (!activeConversationId) {
                setActiveConversationId(response.conversation_id);
                await loadConversations();
            }
        } catch (error) {
            console.error('Error sending message:', error);
            // Remove temp message on error
            setMessages((prev) => prev.filter(msg => msg.id !== tempUserMessage.id));
            alert('Failed to send message. Please make sure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    const handleSelectConversation = (conversationId) => {
        setActiveConversationId(conversationId);
    };

    const handleNewConversation = () => {
        setActiveConversationId(null);
        setMessages([]);
        setInputValue('');
    };

    const handleDeleteConversation = async (conversationId) => {
        try {
            await apiService.deleteConversation(conversationId);

            // Remove from conversations list
            setConversations((prev) => prev.filter((conv) => conv.id !== conversationId));

            // If deleted conversation was active, clear the chat
            if (conversationId === activeConversationId) {
                handleNewConversation();
            }
        } catch (error) {
            console.error('Error deleting conversation:', error);
            alert('Failed to delete conversation. Please try again.');
        }
    };

    const handleSuggestionClick = async (suggestionText) => {
        // Start a new conversation
        handleNewConversation();

        setLoading(true);

        // Optimistically add user message to UI immediately
        const tempUserMessage = {
            id: `temp-${Date.now()}`,
            role: 'user',
            content: suggestionText,
            created_at: new Date().toISOString()
        };
        setMessages([tempUserMessage]);

        try {
            const response = await apiService.sendMessage(null, suggestionText);

            // Replace temp message with real messages from server
            setMessages([
                response.user_message,
                response.assistant_message,
            ]);

            // Set active conversation ID
            setActiveConversationId(response.conversation_id);
            await loadConversations();
        } catch (error) {
            console.error('Error sending suggestion:', error);
            setMessages([]);
            alert('Failed to send message. Please make sure the backend server is running.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex h-screen overflow-hidden bg-gray-50">
            <Sidebar
                conversations={conversations}
                activeConversationId={activeConversationId}
                onSelectConversation={handleSelectConversation}
                onNewConversation={handleNewConversation}
                onDeleteConversation={handleDeleteConversation}
            />
            <div className="flex-1 flex flex-col overflow-hidden">
                <ChatContainer
                    messages={messages}
                    loading={loading}
                    onNewChat={handleNewConversation}
                    onSuggestionClick={handleSuggestionClick}
                />
                <MessageInput
                    value={inputValue}
                    onChange={setInputValue}
                    onSend={handleSendMessage}
                    disabled={loading}
                />
            </div>
        </div>
    );
}

export default App;

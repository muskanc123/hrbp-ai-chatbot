import React, { useEffect, useRef } from 'react';
import Message from './Message';

const ChatContainer = ({ messages, loading, onNewChat, onSuggestionClick }) => {
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    return (
        <div className="flex-1 flex flex-col min-h-0">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 px-8 py-4 flex items-center justify-between shadow-sm flex-shrink-0">
                <h1 className="text-2xl font-bold text-gray-900">My HRBP</h1>
                <button
                    onClick={onNewChat}
                    className="bg-primary-500 hover:bg-primary-600 text-white font-semibold py-2.5 px-5 rounded-lg transition-all shadow-sm hover:shadow-md flex items-center gap-2"
                >
                    <span className="text-lg">+</span>
                    <span>New Chat</span>
                </button>
            </header>

            {/* Messages Container */}
            <div className="flex-1 min-h-0 overflow-y-auto custom-scrollbar px-8 pt-8 pb-6">
                <div className="max-w-4xl mx-auto">
                    {messages.length === 0 && !loading ? (
                        <div className="flex flex-col items-center justify-center h-full min-h-[400px] animate-fade-in">
                            <div className="text-center">
                                <div className="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
                                    <span className="text-4xl">👋</span>
                                </div>
                                <h2 className="text-4xl font-bold text-gray-900 mb-3">
                                    Hello, User!
                                </h2>
                                <p className="text-lg text-gray-600 mb-8">
                                    How can I support you today?
                                </p>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
                                    <div
                                        onClick={() => onSuggestionClick('Show me all employees with their leave balances in a table')}
                                        className="bg-white p-4 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all cursor-pointer"
                                    >
                                        <p className="text-sm font-medium text-gray-700">
                                            📊 Check employee leave balances
                                        </p>
                                    </div>
                                    <div
                                        onClick={() => onSuggestionClick('Show me all employees with their loan information in a table')}
                                        className="bg-white p-4 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all cursor-pointer"
                                    >
                                        <p className="text-sm font-medium text-gray-700">
                                            💰 Review loan information
                                        </p>
                                    </div>
                                    <div
                                        onClick={() => onSuggestionClick('Show me all employees with their performance ratings in a table')}
                                        className="bg-white p-4 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all cursor-pointer"
                                    >
                                        <p className="text-sm font-medium text-gray-700">
                                            ⭐ View performance ratings
                                        </p>
                                    </div>
                                    <div
                                        onClick={() => onSuggestionClick('Give me a summary of all employee data including departments and key metrics')}
                                        className="bg-white p-4 rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-md transition-all cursor-pointer"
                                    >
                                        <p className="text-sm font-medium text-gray-700">
                                            📈 Analyze employee data
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="space-y-6">
                            {messages.map((msg) => (
                                <Message key={msg.id} message={msg} />
                            ))}
                            {loading && (
                                <div className="flex items-start gap-4 animate-fade-in">
                                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-pink-400 to-purple-500 flex items-center justify-center flex-shrink-0 shadow-md">
                                        <span className="text-xl">🤖</span>
                                    </div>
                                    <div className="bg-white rounded-2xl rounded-tl-sm px-6 py-4 shadow-sm border border-gray-100">
                                        <div className="flex gap-2">
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>
        </div>
    );
};

export default ChatContainer;

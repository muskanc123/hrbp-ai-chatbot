import React from 'react';

const Sidebar = ({ conversations, activeConversationId, onSelectConversation, onNewConversation, onDeleteConversation }) => {
    const handleDelete = (e, conversationId) => {
        e.stopPropagation(); // Prevent triggering onSelectConversation
        if (window.confirm('Are you sure you want to delete this conversation?')) {
            onDeleteConversation(conversationId);
        }
    };

    return (
        <div className="w-72 bg-white border-r border-gray-200 flex flex-col h-screen">
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
                        <span className="text-2xl">🧠</span>
                    </div>
                    <span className="text-sm font-bold tracking-wide text-gray-900">
                        CULTURELLIGENCE
                    </span>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-1 overflow-y-auto custom-scrollbar p-4">
                <div className="mb-6">
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-2">
                        MY AGENTS
                    </h3>
                    <ul className="space-y-1">
                        <li className="bg-primary-50 text-primary-700 rounded-lg px-4 py-3 flex items-center gap-3 font-medium border-l-4 border-primary-500">
                            <span className="text-xl">👤</span>
                            <span>My HRBP</span>
                        </li>
                        <li className="text-gray-600 hover:bg-gray-50 rounded-lg px-4 py-3 flex items-center gap-3 font-medium cursor-pointer transition-colors">
                            <span className="text-xl">📊</span>
                            <span>My Leadership Coach</span>
                        </li>
                        <li className="text-gray-600 hover:bg-gray-50 rounded-lg px-4 py-3 flex items-center gap-3 font-medium cursor-pointer transition-colors">
                            <span className="text-xl">🎯</span>
                            <span>My Growth Consultant</span>
                        </li>
                    </ul>
                </div>

                <div>
                    <h3 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-2">
                        PREVIOUS CONVERSATIONS
                    </h3>
                    <div className="space-y-2">
                        {conversations.map((conv) => (
                            <div
                                key={conv.id}
                                onClick={() => onSelectConversation(conv.id)}
                                className={`group px-4 py-3 rounded-lg cursor-pointer transition-all flex items-center justify-between ${conv.id === activeConversationId
                                    ? 'bg-primary-50 border-l-4 border-primary-500 text-primary-700 font-medium'
                                    : 'hover:bg-gray-50 text-gray-700 border-l-4 border-transparent'
                                    }`}
                            >
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm truncate">{conv.title}</p>
                                    <p className="text-xs text-gray-500 mt-1">
                                        {new Date(conv.updated_at).toLocaleDateString()}
                                    </p>
                                </div>
                                <button
                                    onClick={(e) => handleDelete(e, conv.id)}
                                    className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity p-1.5 hover:bg-red-50 rounded-md"
                                    title="Delete conversation"
                                >
                                    <svg className="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </nav>

            {/* New Chat Button */}
            {/* <div className="p-4 border-t border-gray-200">
                <button
                    onClick={onNewConversation}
                    className="w-full bg-primary-500 hover:bg-primary-600 text-white font-semibold py-3 px-4 rounded-lg transition-all shadow-sm hover:shadow-md flex items-center justify-center gap-2"
                >
                    <span className="text-xl">+</span>
                    <span>New Chat</span>
                </button>
            </div> */}
        </div>
    );
};

export default Sidebar;

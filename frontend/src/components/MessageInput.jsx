import React from 'react';

const MessageInput = ({ value, onChange, onSend, disabled }) => {
    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            onSend();
        }
    };

    return (
        <div className="bg-white border-t border-gray-200 px-8 py-6 flex-shrink-0">
            <div className="max-w-4xl mx-auto">
                <div className="flex items-center gap-3 bg-gray-50 rounded-2xl border-2 border-gray-200 focus-within:border-primary-500 focus-within:bg-white transition-all p-2">
                    <input
                        type="text"
                        className="flex-1 bg-transparent px-4 py-3 text-gray-900 placeholder-gray-500 focus:outline-none text-[15px]"
                        placeholder="Ask about your team, HR insights..."
                        value={value}
                        onChange={(e) => onChange(e.target.value)}
                        onKeyPress={handleKeyPress}
                        disabled={disabled}
                    />
                    <button
                        onClick={onSend}
                        disabled={disabled || !value.trim()}
                        className="bg-primary-500 hover:bg-primary-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold px-6 py-3 rounded-xl transition-all shadow-sm hover:shadow-md flex items-center gap-2"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                        <span>Send</span>
                    </button>
                </div>
                <p className="text-xs text-gray-500 mt-3 text-center">
                    AI can make mistakes. Verify important information.
                </p>
            </div>
        </div>
    );
};

export default MessageInput;

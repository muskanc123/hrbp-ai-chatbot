import React from 'react';

const Message = ({ message }) => {
    const isUser = message.role === 'user';

    return (
        <div className={`flex items-start gap-4 animate-fade-in ${isUser ? 'flex-row-reverse' : ''}`}>
            {/* Avatar */}
            <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-md ${isUser
                ? 'bg-gradient-to-br from-primary-500 to-primary-600'
                : 'bg-gradient-to-br from-pink-400 to-purple-500'
                }`}>
                <span className="text-xl">{isUser ? '👤' : '🤖'}</span>
            </div>

            {/* Message Content */}
            <div className={`max-w-2xl ${isUser
                ? 'bg-primary-500 text-white rounded-2xl rounded-tr-sm'
                : 'bg-white text-gray-900 rounded-2xl rounded-tl-sm border border-gray-100'
                } px-6 py-4 shadow-sm`}>
                {isUser ? (
                    <p className="text-[15px] leading-relaxed whitespace-pre-wrap">
                        {message.content}
                    </p>
                ) : (
                    <div
                        className="text-[15px] leading-relaxed prose prose-sm max-w-none prose-table:border-collapse prose-th:border prose-th:border-gray-300 prose-td:border prose-td:border-gray-300 prose-headings:mt-4 prose-headings:mb-2"
                        dangerouslySetInnerHTML={{ __html: message.content }}
                    />
                )}
            </div>
        </div>
    );
};

export default Message;

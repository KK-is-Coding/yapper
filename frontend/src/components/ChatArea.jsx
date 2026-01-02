import React, { useState } from 'react';
import { MessageCircle, MapPin, Send, LogOut } from 'lucide-react';

const ChatArea = ({ selectedRoom, messages, username, onSendMessage, onLogout }) => {
    const [newMessage, setNewMessage] = useState('');

    const handleSend = () => {
        if (newMessage.trim()) {
            onSendMessage(newMessage);
            setNewMessage('');
        }
    };

    if (!selectedRoom) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
                <MessageCircle size={64} className="text-zinc-700 mb-4" />
                <h2 className="text-2xl font-semibold mb-2">Welcome to Chugli</h2>
                <p className="text-zinc-400">Select a room from the list to start chatting</p>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col">
            {/* Chat Header */}
            <div className="h-16 border-b border-zinc-800 px-6 flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-semibold">{selectedRoom.name}</h2>
                    <p className="text-sm text-zinc-400 flex items-center gap-1">
                        <MapPin size={12} />
                        {selectedRoom.location}
                        <span className="ml-2 text-zinc-600">• Room will be visible to users within 5km</span>
                    </p>
                </div>
                <button
                    onClick={onLogout}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-2 transition-colors"
                >
                    <LogOut size={18} />
                    Logout
                </button>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6">
                {messages.length === 0 ? (
                    <div className="h-full flex items-center justify-center text-zinc-500">
                        No messages yet. Start the conversation!
                    </div>
                ) : (
                    <div className="space-y-4">
                        {messages.map(message => (
                            <div
                                key={message.id}
                                className={`flex ${message.sender === username ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`max-w-md px-4 py-2 rounded-lg ${message.sender === username
                                            ? 'bg-orange-600'
                                            : 'bg-zinc-800'
                                        }`}
                                >
                                    <div className="text-xs text-zinc-400 mb-1">{message.sender}</div>
                                    <div>{message.text}</div>
                                    <div className="text-xs text-zinc-400 mt-1">{message.timestamp}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Message Input */}
            <div className="p-6 border-t border-zinc-800">
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Type a message..."
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                        maxLength={300}
                        className="flex-1 px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-orange-500 transition-colors"
                    />
                    <div className="text-sm text-zinc-500 flex items-center px-2">
                        {newMessage.length}/300
                    </div>
                    <button
                        onClick={handleSend}
                        disabled={!newMessage.trim()}
                        className="px-6 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded-lg flex items-center gap-2 transition-colors"
                    >
                        <Send size={18} />
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatArea;
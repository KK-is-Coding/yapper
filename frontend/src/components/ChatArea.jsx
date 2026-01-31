import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, MapPin, Send, LogOut } from 'lucide-react';

const ChatArea = ({ selectedRoom, messages, username, onSendMessage, onLogout }) => {
    const [newMessage, setNewMessage] = useState('');
    const messagesEndRef = useRef(null);

    const normalizedMessages = messages.map((msg) => ({
        id: msg.id,
        sender: msg.sender || msg.username,
        content: msg.content,
        timestamp: msg.timestamp || new Date(msg.created_at).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        }),
    }));

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [normalizedMessages]);

    const handleSend = () => {
        if (!newMessage.trim()) return;
        onSendMessage(newMessage);
        setNewMessage('');
    };

    if (!selectedRoom) {
        return (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
                <MessageCircle size={64} className="text-zinc-700 mb-4" />
                <h2 className="text-2xl font-semibold mb-2">Welcome to Yapper</h2>
                <p className="text-zinc-400">Select a room from the list to start chatting</p>
            </div>
        );
    }

    return (
        <div className="flex-1 flex flex-col h-screen overflow-hidden">
            <div className="h-16 border-b border-zinc-800 px-6 flex items-center justify-between">
                <div>
                    <h2 className="text-xl font-semibold">{selectedRoom.name}</h2>
                    <p className="text-sm text-zinc-400 flex items-center gap-1">
                        <MapPin size={12} />
                        {selectedRoom.location}
                        <span className="ml-2 text-blue-500">• Room visible within 5km</span>
                    </p>
                </div>
                <button
                    onClick={onLogout}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded-lg flex items-center gap-2"
                >
                    <LogOut size={18} />
                    Logout
                </button>
            </div>

            <div className="flex-1 overflow-y-auto p-6">
                {normalizedMessages.length === 0 ? (
                    <div className="h-full flex items-center justify-center text-zinc-500">
                        No messages yet. Start the conversation!
                    </div>
                ) : (
                    <div className="space-y-4">
                        {normalizedMessages.map((message) => {
                            const isMe = message.sender === username;

                            return (
                                <div key={message.id} className={`flex ${isMe ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`flex flex-col max-w-[70%] ${isMe ? 'items-end' : 'items-start'}`}>
                                        <div className="text-xs text-zinc-400 mb-1">
                                            {message.timestamp} &nbsp; {message.sender}
                                        </div>
                                        <div
                                            className={`px-4 py-2 rounded-2xl break-words ${
                                                isMe ? 'bg-orange-600' : 'bg-zinc-800'
                                            }`}
                                        >
                                            {message.content}
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                        <div ref={messagesEndRef} />
                    </div>
                )}
            </div>

            <div className="p-6 border-t border-zinc-800 bg-zinc-950">
                <div className="flex gap-2">
                    <input
                        type="text"
                        placeholder="Type a message..."
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                        maxLength={300}
                        className="flex-1 px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-lg"
                    />
                    <button
                        onClick={handleSend}
                        disabled={!newMessage.trim()}
                        className="px-6 py-3 bg-orange-600 rounded-lg flex items-center gap-2"
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

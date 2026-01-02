import React, { useState } from 'react';
import { Plus, X, MapPin } from 'lucide-react';

const CreateRoomModal = ({ userLocation, onClose, onCreateRoom }) => {
    const [roomName, setRoomName] = useState('');

    const handleCreate = () => {
        onCreateRoom(roomName);
        setRoomName('');
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-zinc-800 rounded-xl p-6 max-w-md w-full">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center">
                        <Plus size={20} />
                    </div>
                    <h2 className="text-xl font-semibold">Create New Room</h2>
                    <button
                        onClick={onClose}
                        className="ml-auto p-1 hover:bg-zinc-700 rounded transition-colors"
                    >
                        <X size={20} />
                    </button>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-2">Room Name</label>
                        <input
                            type="text"
                            placeholder="e.g., Coffee Shop Chat, Study Group..."
                            value={roomName}
                            onChange={(e) => setRoomName(e.target.value)}
                            maxLength={50}
                            className="w-full px-4 py-3 bg-zinc-900 border border-orange-600 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-orange-500 transition-colors"
                        />
                        <p className="text-xs text-zinc-500 mt-1">{roomName.length}/50 characters</p>
                    </div>

                    <div className="bg-zinc-900 rounded-lg p-4">
                        <div className="flex items-center gap-2 text-orange-500 mb-2">
                            <MapPin size={18} />
                            <span className="font-medium">Your Location</span>
                        </div>
                        <p className="text-sm text-zinc-400">{userLocation.lat.toFixed(5)}, {userLocation.lng.toFixed(5)}</p>
                        <p className="text-xs text-zinc-500 mt-2">Room will be visible to users within 5km</p>
                    </div>

                    <div className="flex gap-3 pt-2">
                        <button
                            onClick={onClose}
                            className="flex-1 px-4 py-3 bg-zinc-700 hover:bg-zinc-600 rounded-lg transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            onClick={handleCreate}
                            disabled={!roomName.trim()}
                            className="flex-1 px-4 py-3 bg-orange-600 hover:bg-orange-700 disabled:bg-zinc-700 disabled:cursor-not-allowed rounded-lg transition-colors"
                        >
                            Create Room
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CreateRoomModal;
import React from 'react';
import { Plus, RefreshCw } from 'lucide-react';
import RoomList from './RoomList';

const Sidebar = ({ rooms, selectedRoom, onSelectRoom, onCreateRoom, onRefresh }) => {
    return (
        <div className="w-80 bg-zinc-900 border-r border-zinc-800 flex flex-col">
            {/* Sidebar Header */}
            <div className="p-4 border-b border-zinc-800">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold">Nearby Rooms</h2>
                    <button
                        onClick={onRefresh}
                        className="p-2 hover:bg-zinc-800 rounded-lg transition-colors"
                    >
                        <RefreshCw size={18} />
                    </button>
                </div>
                <p className="text-sm text-zinc-400">{rooms.length} rooms available</p>
            </div>

            {/* Create Room Button */}
            <div className="p-4">
                <button
                    onClick={onCreateRoom}
                    className="w-full px-4 py-3 bg-orange-600 hover:bg-orange-700 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
                >
                    <Plus size={20} />
                    Create Room
                </button>
            </div>

            {/* Rooms List */}
            <RoomList
                rooms={rooms}
                selectedRoom={selectedRoom}
                onSelectRoom={onSelectRoom}
            />
        </div>
    );
};

export default Sidebar;
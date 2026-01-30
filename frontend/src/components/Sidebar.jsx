import React from 'react';
import { Plus, RefreshCw } from 'lucide-react';
import RoomList from './RoomList';

const Sidebar = ({ rooms, selectedRoom, onSelectRoom, onCreateRoom, onRefresh }) => {
    return (
        <div className="w-80 bg-zinc-900 border-r border-zinc-800 flex flex-col">
            <div className="p-4 border-b border-zinc-800">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold">Nearby Rooms</h2>
                    <button onClick={onRefresh} className="p-2 hover:bg-zinc-800 rounded-lg">
                        <RefreshCw size={18} />
                    </button>
                </div>
                <p className="text-sm text-zinc-400">{rooms.length} rooms available</p>
            </div>

            <div className="p-4">
                <button
                    onClick={onCreateRoom}
                    className="w-full px-4 py-3 bg-orange-600 rounded-lg"
                >
                    <Plus size={20} /> Create Room
                </button>
            </div>

            <RoomList
                rooms={rooms}
                selectedRoom={selectedRoom}
                onSelectRoom={onSelectRoom}
            />
        </div>
    );
};

export default Sidebar;

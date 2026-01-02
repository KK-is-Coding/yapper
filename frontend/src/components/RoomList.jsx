import React from 'react';
import { MessageCircle, MapPin, Users } from 'lucide-react';

const RoomList = ({ rooms, selectedRoom, onSelectRoom }) => {
    if (rooms.length === 0) {
        return (
            <div className="flex-1 overflow-y-auto">
                <div className="flex flex-col items-center justify-center p-8 text-center">
                    <Users size={48} className="text-zinc-600 mb-4" />
                    <h3 className="text-lg font-medium text-zinc-300 mb-2">No rooms nearby</h3>
                    <p className="text-sm text-zinc-500">Be the first to create one!</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto">
            <div className="space-y-1 p-2">
                {rooms.map(room => (
                    <button
                        key={room.id}
                        onClick={() => onSelectRoom(room)}
                        className={`w-full p-4 rounded-lg text-left transition-colors ${selectedRoom?.id === room.id
                                ? 'bg-orange-600'
                                : 'bg-zinc-800 hover:bg-zinc-750'
                            }`}
                    >
                        <div className="flex items-start gap-3">
                            <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center flex-shrink-0">
                                <MessageCircle size={20} />
                            </div>
                            <div className="flex-1 min-w-0">
                                <h3 className="font-medium truncate">{room.name}</h3>
                                <p className="text-sm text-zinc-400 flex items-center gap-1">
                                    <MapPin size={12} />
                                    {room.location}
                                </p>
                            </div>
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default RoomList;
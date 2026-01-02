import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import CreateRoomModal from './components/CreateRoomModal';

const App = () => {
  const [currentView, setCurrentView] = useState('landing');
  const [username, setUsername] = useState('');
  const [showCreateRoom, setShowCreateRoom] = useState(false);
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [messages, setMessages] = useState({});
  const [userLocation] = useState({ lat: 13.0125, lng: 80.2452 });

  const handleStartChatting = (name) => {
    if (name.trim()) {
      setUsername(name);
      setCurrentView('app');
    }
  };

  const handleCreateRoom = (roomName) => {
    if (roomName.trim()) {
      const newRoom = {
        id: Date.now(),
        name: roomName,
        location: `${userLocation.lat.toFixed(4)}, ${userLocation.lng.toFixed(4)}`,
        lat: userLocation.lat,
        lng: userLocation.lng
      };
      setRooms([...rooms, newRoom]);
      setMessages({ ...messages, [newRoom.id]: [] });
      setShowCreateRoom(false);
      setSelectedRoom(newRoom);
    }
  };

  const handleSendMessage = (messageText) => {
    if (messageText.trim() && selectedRoom) {
      const message = {
        id: Date.now(),
        text: messageText,
        sender: username,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages({
        ...messages,
        [selectedRoom.id]: [...(messages[selectedRoom.id] || []), message]
      });
    }
  };

  const handleLogout = () => {
    setUsername('');
    setCurrentView('landing');
    setRooms([]);
    setSelectedRoom(null);
    setMessages({});
  };

  if (currentView === 'landing') {
    return <LandingPage onStartChatting={handleStartChatting} />;
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex">
      <Sidebar
        rooms={rooms}
        selectedRoom={selectedRoom}
        onSelectRoom={setSelectedRoom}
        onCreateRoom={() => setShowCreateRoom(true)}
        onRefresh={() => setRooms([...rooms])}
      />
      
      <ChatArea
        selectedRoom={selectedRoom}
        messages={messages[selectedRoom?.id] || []}
        username={username}
        onSendMessage={handleSendMessage}
        onLogout={handleLogout}
      />

      {showCreateRoom && (
        <CreateRoomModal
          userLocation={userLocation}
          onClose={() => setShowCreateRoom(false)}
          onCreateRoom={handleCreateRoom}
        />
      )}
    </div>
  );
};

export default App;
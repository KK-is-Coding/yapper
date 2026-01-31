import React, { useEffect, useState, useRef } from 'react';
import LandingPage from './components/LandingPage';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import CreateRoomModal from './components/CreateRoomModal';

const API_BASE = import.meta.env.VITE_API_BASE;

const App = () => {
  const [currentView, setCurrentView] = useState('landing');
  const [username, setUsername] = useState('');
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [messages, setMessages] = useState([]);
  const [showCreateRoom, setShowCreateRoom] = useState(false);
  const [userLocation, setUserLocation] = useState(null);

  const wsRef = useRef(null);

  // stable client id
  const clientIdRef = useRef(
    localStorage.getItem("client_id") ||
    (() => {
      const id = "client_" + Math.random().toString(36).slice(2);
      localStorage.setItem("client_id", id);
      return id;
    })()
  );
  const clientId = clientIdRef.current;

  /* ---------------- LANDING ---------------- */

  const handleStartChatting = (name) => {
    if (!name.trim()) return;
    setUsername(name.trim());
    setCurrentView('app');
  };

  /* ---------------- LOCATION ---------------- */

  useEffect(() => {
    if (currentView !== 'app') return;

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setUserLocation({
          lat: pos.coords.latitude,
          lng: pos.coords.longitude,
        });
      },
      () => alert('Location permission required')
    );
  }, [currentView]);

  /* ---------------- ROOMS ---------------- */

  const fetchRooms = async () => {
    if (!userLocation) return;

    const res = await fetch(
      `${API_BASE}/rooms/nearby?lat=${userLocation.lat}&lon=${userLocation.lng}`
    );
    const data = await res.json();
    setRooms(Array.isArray(data) ? data : []);
  };

  useEffect(() => {
    if (!userLocation) return;
    fetchRooms();
  }, [userLocation]);

  const handleCreateRoom = async (roomName) => {
    if (!userLocation) return;

    const res = await fetch(`${API_BASE}/rooms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: roomName,
        latitude: userLocation.lat,
        longitude: userLocation.lng,
      }),
    });

    const room = await res.json();
    setShowCreateRoom(false);
    await fetchRooms();
    joinRoom(room);
  };

  /* ---------------- WEBSOCKET ---------------- */

  const joinRoom = async (room) => {
    setSelectedRoom(room);
    setMessages([]);

    if (wsRef.current) {
      wsRef.current.close();
    }

    const res = await fetch(`${API_BASE}/rooms/${room.id}/messages/`);
    const history = await res.json();

    const normalizedHistory = history.map((m) => ({
      id: m.id,
      sender: m.username,
      content: m.content,
      timestamp: m.created_at,
    }));

    setMessages(normalizedHistory);

    const ws = new WebSocket(
      import.meta.env.VITE_WS_BASE + `/ws/${room.id}`
    );


    ws.onopen = () => {
      ws.send(
        JSON.stringify({
          type: "join",
          nickname: username,
          client_id: clientId,
        })
      );
    };

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);

      if (msg.type === "error") {
        alert(msg.message);
        return;
      }

      if (msg.type === "message") {
        setMessages((prev) => [
          ...prev,
          {
            id: msg.id,
            sender: msg.sender,
            content: msg.content,
            timestamp: msg.timestamp,
          },
        ]);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    wsRef.current = ws;
  };

  const handleSendMessage = (text) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;

    wsRef.current.send(
      JSON.stringify({
        type: "message",
        content: text,
      })
    );
  };

  const handleLogout = () => {
    wsRef.current?.close();
    setCurrentView('landing');
    setUsername('');
    setRooms([]);
    setMessages([]);
    setSelectedRoom(null);
  };

  if (currentView === 'landing') {
    return <LandingPage onStartChatting={handleStartChatting} />;
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex">
      <Sidebar
        rooms={rooms}
        selectedRoom={selectedRoom}
        onSelectRoom={joinRoom}
        onCreateRoom={() => setShowCreateRoom(true)}
        onRefresh={fetchRooms}
      />

      <ChatArea
        selectedRoom={selectedRoom}
        messages={messages}
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

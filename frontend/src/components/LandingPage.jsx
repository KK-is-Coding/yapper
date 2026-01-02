import React, { useState, useEffect } from 'react';

const LandingPage = ({ onStartChatting }) => {
    const [username, setUsername] = useState('');
    const [particles, setParticles] = useState([]);

    useEffect(() => {
        const newParticles = Array.from({ length: 6 }, (_, i) => ({
            id: i,
            x: Math.random() * 100,
            y: Math.random() * 100,
            size: Math.random() * 8 + 4,
            color: ['#00f5ff', '#ffeb3b', '#ff6ec7', '#ff9800'][Math.floor(Math.random() * 4)],
            duration: Math.random() * 3 + 2
        }));
        setParticles(newParticles);
    }, []);

    const handleSubmit = () => {
        onStartChatting(username);
    };

    return (
        <div className="min-h-screen bg-zinc-950 text-white flex items-center justify-center p-8">
            <div className="w-full max-w-6xl flex items-center justify-between gap-16">
                {/* Left side - Content */}
                <div className="flex-1 space-y-8">
                    <div>
                        <h1 className="text-7xl font-serif mb-4">
                            <div>Impossible?</div>
                            <div>Possible.</div>
                        </h1>
                        <p className="text-zinc-400 text-lg">Connect with people nearby</p>
                    </div>

                    <div className="space-y-4 max-w-md">
                        <input
                            type="text"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
                            className="w-full px-6 py-4 bg-zinc-800 border border-zinc-700 rounded-lg text-white placeholder-zinc-500 focus:outline-none focus:border-orange-500 transition-colors"
                        />
                        <button
                            onClick={handleSubmit}
                            disabled={!username.trim()}
                            className="w-full px-6 py-4 bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed rounded-lg font-medium transition-colors"
                        >
                            Start Chatting
                        </button>
                    </div>
                </div>

                {/* Right side - Animated panel */}
                <div className="flex-1 relative">
                    <div className="aspect-[4/5] bg-gradient-to-br from-orange-500 via-orange-600 to-orange-700 rounded-3xl overflow-hidden relative">
                        {/* Gradient overlay */}
                        <div className="absolute inset-0 bg-gradient-to-br from-orange-400/30 via-transparent to-red-600/30"></div>

                        {/* Animated particles */}
                        {particles.map(particle => (
                            <div
                                key={particle.id}
                                className="absolute rounded-full animate-pulse"
                                style={{
                                    left: `${particle.x}%`,
                                    top: `${particle.y}%`,
                                    width: `${particle.size}px`,
                                    height: `${particle.size}px`,
                                    backgroundColor: particle.color,
                                    animationDuration: `${particle.duration}s`
                                }}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
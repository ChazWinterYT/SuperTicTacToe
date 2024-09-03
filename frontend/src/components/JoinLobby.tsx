import React, { useState } from 'react';
import axios from 'axios';
import '../styles/JoinLobby.css';

const BASE_URL = process.env.REACT_APP_TIC_TAC_TOE_API_BASE_URL;

interface JoinLobbyProps {
    onJoin: (playerId: string) => void;
}

interface JoinLobbyResponse {
    player_id: string;
}

const JoinLobby: React.FC<JoinLobbyProps> = ({ onJoin }) => {
    const [playerName, setPlayerName] = useState("");

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (playerName.trim()) {
            try {
                const response = await axios.post<JoinLobbyResponse>(
                    `${BASE_URL}/lobby/join?player_name=${playerName.trim()}`,
                );
                const playerId = response.data.player_id;
                onJoin(playerId);
            } catch (error) {
                console.error("Error joining lobby:", error);
            }
        }
    };

    return (
        <div className="join-lobby-container">
            <h2>Enter Your Name</h2>
            <form onSubmit={handleSubmit} className="join-lobby-form">
                <input
                    type="text"
                    value={playerName}
                    onChange={(e) => setPlayerName(e.target.value)}
                    placeholder="Your name"
                    className="join-lobby-input"
                />
                <button type="submit" className="join-lobby-button">
                    Join Lobby
                </button>
            </form>
        </div>
    );
};

export default JoinLobby;

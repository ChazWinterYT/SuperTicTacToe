import React, { useState } from 'react';
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_TIC_TAC_TOE_API_BASE_URL;

interface JoinLobbyProps {
    onJoin: (playerId: string) => void;
}

interface JoinLobbyResponse {
    player_id: string;
}

const JoinLobby: React.FC<JoinLobbyProps> = ({ onJoin }) => {
    const [playerName, setPlayerName] = useState('');

    const handleJoin = async () => {
        try {
            const response = await axios.post<JoinLobbyResponse>(
                `${BASE_URL}/lobby/join?player_name=${playerName}`
            );
            const playerId = response.data.player_id;
            onJoin(playerId);
        } catch (error) {
            console.error('Error joining lobby:', error);
        }
    };

    return (
        <div>
            <input
                type="text"
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
                placeholder="Enter your name"
            />
            <button onClick={handleJoin}>Join Lobby</button>
        </div>
    );
};

export default JoinLobby;

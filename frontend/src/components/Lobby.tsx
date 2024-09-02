import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Lobby.css'

const BASE_URL = process.env.REACT_APP_TIC_TAC_TOE_API_BASE_URL;

interface Player {
    id: string;
    name: string;
}

interface LobbyPlayersReponse {
    players: Player[];
}

interface LobbyProps {
    playerId: string;
    onChallenge: (challengedPlayerId: string) => void;
}

const Lobby: React.FC<LobbyProps> = ({ playerId, onChallenge }) => {
    const [players, setPlayers] = useState<Player[]>([]);

    // Fetch the list of players in the lobby
    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                const response = await axios.get<LobbyPlayersReponse>(
                    `${BASE_URL}/lobby/players`
                );
                setPlayers(response.data.players);
            } catch (error) {
                console.error("Error fetching players:", error);
            }
        };

        fetchPlayers();

        // Refresh the list of players after specified interval
        const interval = setInterval(fetchPlayers, 3000);
        return () => clearInterval(interval);
    }, []);

    const handleChallenge = (challengedPlayerId: string) => {
        onChallenge(challengedPlayerId);
    };

    return (
        <div className="lobby">
            <h2>Player Lobby</h2>
            <ul>
                {players.map((player) => (
                    <li key={player.id}>
                        {player.name} {player.id === playerId && "(You)"}
                        {player.id !== playerId && (
                            <button onClick={() => handleChallenge(player.id)}>Challenge</button>
                        )}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Lobby;
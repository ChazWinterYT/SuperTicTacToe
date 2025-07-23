import React, { useContext, useState } from 'react';
import { PlayerContext } from '../contexts/PlayerContext';
import { joinLobby } from '../api/endpoints/lobby';

const JoinPage: React.FC = () => {
  const { player, setPlayer } = useContext(PlayerContext)!;
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGuestJoin = async () => {
    if (!player) return;
    setLoading(true);
    setError(null);
    try {
      const response = await joinLobby(player.displayName) as { playerId: string };
      // Assuming response contains player playerId or similar info
      setPlayer({ ...player, playerId: response.playerId, isGuest: true });
      // Redirect to lobby or other page can be handled here
    } catch (err) {
      setError('Failed to join lobby');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Join Lobby</h1>
      {player && (
        <button onClick={handleGuestJoin} disabled={loading}>
          {loading ? 'Joining...' : `Join as ${player.displayName}`}
        </button>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default JoinPage;

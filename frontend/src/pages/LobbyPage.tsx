import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Lobby from "../components/Lobby";
import { usePlayer } from "../contexts/PlayerContext";

const LobbyPage: React.FC = () => {
  const { player } = usePlayer();
  const navigate = useNavigate();

  useEffect(() => {
    if (!player?.playerId) {
      navigate("/", { replace: true });
    }
  }, [player, navigate]);

  // Placeholder for onChallenge, can be expanded later
  const handleChallenge = (challengedPlayerId: string) => {
    // This will be handled in a later milestone
  };

  if (!player?.playerId) return null;

  return (
    <div>
      <Lobby playerId={player.playerId} onChallenge={handleChallenge} />
    </div>
  );
};

export default LobbyPage;

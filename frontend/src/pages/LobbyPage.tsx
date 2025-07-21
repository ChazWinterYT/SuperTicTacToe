import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Lobby from "../components/Lobby";
import { usePlayer } from "../contexts/PlayerContext";

const LobbyPage: React.FC = () => {
  const { playerId } = usePlayer();
  const navigate = useNavigate();

  useEffect(() => {
    if (!playerId) {
      navigate("/", { replace: true });
    }
  }, [playerId, navigate]);

  // Placeholder for onChallenge, can be expanded later
  const handleChallenge = (challengedPlayerId: string) => {
    // This will be handled in a later milestone
  };

  if (!playerId) return null;

  return (
    <div>
      <Lobby playerId={playerId} onChallenge={handleChallenge} />
    </div>
  );
};

export default LobbyPage;

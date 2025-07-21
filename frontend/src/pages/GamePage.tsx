import React, { useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TicTacToeBoard3x3 from "../components/TicTacToeBoard3x3";
import { usePlayer } from "../contexts/PlayerContext";

const GamePage: React.FC = () => {
  const { playerId } = usePlayer();
  const { gameId } = useParams<{ gameId: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    if (!playerId) {
      navigate("/", { replace: true });
    }
  }, [playerId, navigate]);

  if (!playerId || !gameId) return null;

  return (
    <div>
      <TicTacToeBoard3x3 gameId={gameId} player={playerId} />
    </div>
  );
};

export default GamePage;

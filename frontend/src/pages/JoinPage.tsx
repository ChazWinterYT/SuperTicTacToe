import React from "react";
import JoinLobby from "../components/JoinLobby";
import { usePlayer } from "../contexts/PlayerContext";

const JoinPage: React.FC = () => {
  const { setPlayerId } = usePlayer();

  // Pass setPlayerId to JoinLobby's onJoin
  return (
    <div>
      <JoinLobby onJoin={setPlayerId} />
    </div>
  );
};

export default JoinPage;

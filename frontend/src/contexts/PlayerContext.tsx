import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface PlayerContextType {
  playerId: string | null;
  setPlayerId: (id: string | null) => void;
}

const PlayerContext = createContext<PlayerContextType | undefined>(undefined);

export const PlayerProvider = ({ children }: { children: ReactNode }) => {
  const [playerId, setPlayerIdState] = useState<string | null>(() => {
    return localStorage.getItem("playerId");
  });

  useEffect(() => {
    if (playerId) {
      localStorage.setItem("playerId", playerId);
    } else {
      localStorage.removeItem("playerId");
    }
  }, [playerId]);

  const setPlayerId = (id: string | null) => {
    setPlayerIdState(id);
  };

  return (
    <PlayerContext.Provider value={{ playerId, setPlayerId }}>
      {children}
    </PlayerContext.Provider>
  );
};

export const usePlayer = (): PlayerContextType => {
  const context = useContext(PlayerContext);
  if (!context) {
    throw new Error("usePlayer must be used within a PlayerProvider");
  }
  return context;
};

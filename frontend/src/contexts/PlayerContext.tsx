import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { randomName } from '../utils/randomName';

interface Player {
  playerId: string;
  displayName: string;
  isGuest: boolean;
}

interface PlayerContextType {
  player: Player | null;
  setPlayer: React.Dispatch<React.SetStateAction<Player | null>>;
}

export const PlayerContext = createContext<PlayerContextType | undefined>(undefined);

export const PlayerProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [player, setPlayer] = useState<Player | null>(null);

  useEffect(() => {
    // Load player from localStorage or create guest
    const storedPlayer = localStorage.getItem('player');
    if (storedPlayer) {
      setPlayer(JSON.parse(storedPlayer));
    } else {
      const guestPlayer: Player = {
        playerId: crypto.randomUUID(),
        displayName: randomName(),
        isGuest: true,
      };
      setPlayer(guestPlayer);
      localStorage.setItem('player', JSON.stringify(guestPlayer));
    }
  }, []);

  useEffect(() => {
    if (player) {
      localStorage.setItem('player', JSON.stringify(player));
    }
  }, [player]);

  return (
    <PlayerContext.Provider value={{ player, setPlayer }}>
      {children}
    </PlayerContext.Provider>
  );
};

// Add usePlayer hook for convenience
import { useContext } from 'react';

export function usePlayer() {
  const context = useContext(PlayerContext);
  if (!context) {
    throw new Error('usePlayer must be used within a PlayerProvider');
  }
  return context;
}

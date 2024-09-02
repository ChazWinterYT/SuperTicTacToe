import React, { useState } from 'react';
import './App.css';
import TicTacToeBoard3x3 from './components/TicTacToeBoard3x3';
import Version from './components/Version';
import JoinLobby from './components/JoinLobby';
import Lobby from './components/Lobby';

function App() {
  const [playerId, setPlayerId] = useState<string | null>(null);
  const [gameId, setGameId] = useState<string | null>(null);

  // Handle when a player joins the lobby
  const handleJoinLobby = (id: string) => {
    setPlayerId(id);
  };

  // Handle when a player challenges another player
  const handleChallenge = (challengedPlayerId: string) => {
    // Generate or retrieve a game ID
    const newGameId = `game_${Date.now()}`;
    setGameId(newGameId);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Super Tic Tac Toe!</h2>
      </header>
      <div className='main-content'>
        {gameId && playerId ? (
          <TicTacToeBoard3x3 gameId={gameId} player={playerId} />
        ) : playerId ? (
          <Lobby playerId={playerId} onChallenge={handleChallenge} />
        ) : (
          <JoinLobby onJoin={handleJoinLobby} />
        )}
      </div>
      <Version />
    </div>
  );
}

export default App;

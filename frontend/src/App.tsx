import React from 'react';
import './App.css';
import TicTacToeBoard3x3 from './components/TicTacToeBoard3x3';
import Version from './components/Version';

function App() {
  const gameId = "placeholder-game-id";
  const player = "X";

  return (
    <div className="App">
      <header className="App-header">
        <p>
          Super Tic Tac Toe!
        </p>
      </header>
      <div className='main-content'>
        <TicTacToeBoard3x3 gameId={gameId} player={player} />
      </div>
      <Version />
    </div>
  );
}

export default App;

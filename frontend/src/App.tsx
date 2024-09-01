import React from 'react';
import './App.css';
import TicTacToeBoard3x3 from './TicTacToeBoard3x3';
import Version from './Version';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Super Tic Tac Toe!
        </p>
      </header>
      <TicTacToeBoard3x3 />
      <Version />
    </div>
  );
}

export default App;

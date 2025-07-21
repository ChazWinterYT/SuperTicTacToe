import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { PlayerProvider } from "./contexts/PlayerContext";
import JoinPage from "./pages/JoinPage";
import LobbyPage from "./pages/LobbyPage";
import GamePage from "./pages/GamePage";
import NotFoundPage from "./pages/NotFoundPage";
import Version from "./components/Version";

function App() {
  return (
    <PlayerProvider>
      <div className="App">
        <header className="App-header">
          <h2>Super Tic Tac Toe!</h2>
        </header>
        <div className="main-content">
          <BrowserRouter basename="/SuperTicTacToe/frontend">
            <Routes>
              <Route path="/" element={<JoinPage />} />
              <Route path="/join" element={<Navigate to="/" replace />} />
              <Route path="/lobby" element={<LobbyPage />} />
              <Route path="/game/:gameId" element={<GamePage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </BrowserRouter>
        </div>
        <Version />
      </div>
    </PlayerProvider>
  );
}

export default App;

import React from 'react';
import { Routes as RouterRoutes, Route, Navigate } from 'react-router-dom';

// Placeholder components for pages
const JoinPage = () => <div>Join Page (stub)</div>;
const LobbyPage = () => <div>Lobby Page (coming soon)</div>;
const GamePage = () => <div>Game Page (stub)</div>;
const NotFoundPage = () => <div>404 - Not Found</div>;

// RequirePlayer route guard stub
const RequirePlayer: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // TODO: Implement PlayerContext check
  const playerExists = true; // stub: always allow for now

  if (!playerExists) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
};

export default function Routes() {
  return (
    <RouterRoutes>
      <Route path="/" element={<JoinPage />} />
      <Route
        element={<RequirePlayer><></></RequirePlayer>}
      >
        <Route path="/lobby" element={<LobbyPage />} />
        <Route path="/game/:gameId" element={<GamePage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </RouterRoutes>
  );
}

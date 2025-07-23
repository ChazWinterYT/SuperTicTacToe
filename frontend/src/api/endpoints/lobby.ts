import apiClient from '../rest';

export async function joinLobby(displayName: string) {
  const response = await apiClient.post('/lobby/join', { player_name: displayName });
  return response.data;
}

export async function leaveLobby(playerId: string) {
  const response = await apiClient.delete(`/lobby/leave/${playerId}`);
  return response.data;
}

export async function getLobbyPlayers() {
  const response = await apiClient.get('/lobby/players');
  return (response.data as any).players;
}

export async function challengePlayer(challengerId: string, challengedId: string) {
  const response = await apiClient.post(`/lobby/challenge/${challengerId}`, { challenged_player_id: challengedId });
  return response.data;
}

// Add other lobby-related API functions as needed

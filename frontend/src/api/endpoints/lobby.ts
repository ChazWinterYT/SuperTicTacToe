import apiClient from '../rest';

export async function joinLobby(displayName: string) {
  const response = await apiClient.post('/lobby/join', { player_name: displayName });
  return response.data;
}

export async function leaveLobby(playerId: string) {
  const response = await apiClient.delete(`/lobby/leave/${playerId}`);
  return response.data;
}

// Add other lobby-related API functions as needed

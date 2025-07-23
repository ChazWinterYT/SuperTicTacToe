import apiClient from '../rest';

export async function joinLobby(name: string) {
  const response = await apiClient.post('/lobby/join', { name });
  return response.data;
}

export async function leaveLobby(id: string) {
  const response = await apiClient.delete(`/lobby/leave/${id}`);
  return response.data;
}

// Add other lobby-related API functions as needed

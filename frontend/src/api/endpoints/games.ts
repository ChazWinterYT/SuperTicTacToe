import apiClient from '../rest';

export async function createGame(creatorId: string, payload: any) {
  const response = await apiClient.post(`/games/create/${creatorId}`, payload);
  return response.data;
}

export async function joinGame(gameId: string, playerId: string) {
  const response = await apiClient.post(`/games/${gameId}/join/${playerId}`);
  return response.data;
}

export async function startGame(gameId: string, playerId: string) {
  const response = await apiClient.post(`/games/${gameId}/start/${playerId}`);
  return response.data;
}

export async function makeMove(gameId: string, playerId: string, position: number) {
  const response = await apiClient.post(`/games/${gameId}/move/${playerId}`, { position });
  return response.data;
}

export async function getGame(gameId: string) {
  const response = await apiClient.get(`/games/${gameId}`);
  return response.data;
}

export async function getPublicGames() {
  const response = await apiClient.get('/games/public');
  return response.data;
}

export async function deleteGame(gameId: string, playerId: string) {
  const response = await apiClient.delete(`/games/${gameId}/${playerId}`);
  return response.data;
}

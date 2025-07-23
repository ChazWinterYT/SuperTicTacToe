import apiClient from '../rest';

export async function createGame(creatorId: string, payload: any) {
  const response = await apiClient.post(`/games/create/${creatorId}`, payload);
  return response.data;
}

export async function joinGame(id: string, player: string) {
  const response = await apiClient.post(`/games/${id}/join/${player}`);
  return response.data;
}

export async function startGame(id: string, player: string) {
  const response = await apiClient.post(`/games/${id}/start/${player}`);
  return response.data;
}

export async function makeMove(id: string, player: string, pos: any) {
  const response = await apiClient.post(`/games/${id}/move/${player}`, pos);
  return response.data;
}

export async function getGame(id: string) {
  const response = await apiClient.get(`/games/${id}`);
  return response.data;
}

export async function getPublicGames() {
  const response = await apiClient.get('/games/public');
  return response.data;
}

export async function deleteGame(id: string, player: string) {
  const response = await apiClient.delete(`/games/${id}/${player}`);
  return response.data;
}

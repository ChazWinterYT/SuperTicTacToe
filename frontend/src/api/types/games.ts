export interface GameResponse {
  gameId: string;
  // Additional fields matching FastAPI GameResponse
  // e.g., creatorId, players, status, etc.
}

export interface GameState {
  board: any; // Define the board structure as needed (e.g., 2D array or other type)
  status: string;
  currentTurn: string;
  // Add other game state fields as required
}

export interface PublicGamesResponse {
  games: GameResponse[];
}

export interface MakeMoveRequest {
  position: number;
}

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Optional
from .game_logic import check_winner, is_board_full

router = APIRouter()

class ConnectionManager:
    def __init__(self) -> None:
        # Maps game_id to a list of connected WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # Maps game_id to its current state
        self.game_states: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
            self.game_states[game_id] = {
                "board": [None] * 9,
                "isXNext": True,
                "winner": None,
                "isDraw": False,
            }
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        self.active_connections[game_id].remove(websocket)
        if not self.active_connections[game_id]:
            del self.active_connections[game_id]
            del self.game_states[game_id]

    async def send_game_state(self, game_id: str):
        game_state = self.game_states[game_id]
        message = {
            "board": game_state["board"],
            "isXNext": game_state["isXNext"],
            "winner": game_state["winner"],
            "isDraw": game_state["isDraw"],
        }
        for connection in self.active_connections[game_id]:
            await connection.send_json(message)

    async def handle_move(self, game_id: str, index: int, player: str):
        game_state = self.game_states[game_id]
        board = game_state["board"]

        # Don't allow moves on occupied squares or if the game is over
        if board[index] is not None or game_state["winner"] is not None:
            return
        
        board[index] = player
        game_state["isXNext"] = not game_state["isXNext"]

        # Check for a winner or if the game is a draw
        winner = check_winner(board)
        if winner:
            game_state["winner"] = winner
        elif is_board_full(board):
            game_state["isDraw"] = True

        await self.send_game_state(game_id)

manager = ConnectionManager()

@router.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: str):
    await manager.connect(websocket, game_id)
    await manager.send_game_state(game_id)
    try:
        while True:
            data = await websocket.receive_json()
            index = data.get("index")
            if index is not None and player in ["X", "O"]:
                await manager.handle_move(game_id, index, player)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, game_id)

@router.get("/api/game/start")
async def start_game():
    return {"message": "Game started"}

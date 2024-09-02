from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .game_logic import GameManager

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.lobby: dict[str, str] = {}

    async def connect(self, websocket: WebSocket, player_id: str, player_name: str):
        await websocket.accept()
        self.active_connections[player_id] = websocket
        self.lobby[player_id] = player_name

    def disconnect(self, player_id: str):
        if player_id in self.active_connections:
            del self.active_connections[player_id]
            if player_id in self.lobby:
                del self.lobby[player_id]

    async def broadcast_lobby_state(self):
        lobby_state = {
            "players": [{
                "id": player_id,
                "name": player_name
            } for player_id, player_name in self.lobby.items]
        }
        for connection in self.active_connections.values():
            await connection.send_json(lobby_state)

    async def send_personal_message(self, message: str, player_id: str):
        websocket = self.active_connections.get(player_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()
game_manager = GameManager()  # Instance of GameManager from game_logic.py

@router.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    await manager.connect(websocket, player_id)
    try:
        while True:
            data = await websocket.receive_json()
            index = data.get("index")
            if index is not None:
                # Delegate the move handling to game_logic
                game_state = game_manager.handle_move(game_id, index, player_id)
                await manager.broadcast(game_state)
    except WebSocketDisconnect:
        manager.disconnect(player_id)
        await manager.broadcast_lobby_state

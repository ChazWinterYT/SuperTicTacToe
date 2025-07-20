from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.core.exceptions import WebSocketError
from app.services.game_service import GameService
from app.services.lobby_service import LobbyService
from app.repositories.implementations.dynamodb_player_repository import DynamoDBPlayerRepository
from app.repositories.implementations.dynamodb_game_repository import DynamoDBGameRepository


class ConnectionManager:
    """Manages WebSocket connections for real-time communication."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.player_connections: Dict[str, str] = {}  # player_id -> connection_id
        self.game_connections: Dict[str, Set[str]] = {}  # game_id -> set of player_ids
    
    async def connect(self, websocket: WebSocket, player_id: str) -> str:
        """Connect a player to the WebSocket."""
        await websocket.accept()
        
        connection_id = f"conn_{player_id}_{id(websocket)}"
        self.active_connections[connection_id] = websocket
        self.player_connections[player_id] = connection_id
        
        return connection_id
    
    def disconnect(self, player_id: str) -> None:
        """Disconnect a player from the WebSocket."""
        if player_id in self.player_connections:
            connection_id = self.player_connections[player_id]
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            del self.player_connections[player_id]
    
    async def send_personal_message(self, message: dict, player_id: str) -> None:
        """Send a message to a specific player."""
        if player_id in self.player_connections:
            connection_id = self.player_connections[player_id]
            if connection_id in self.active_connections:
                websocket = self.active_connections[connection_id]
                await websocket.send_json(message)
    
    async def send_to_game(self, message: dict, game_id: str) -> None:
        """Send a message to all players in a game."""
        if game_id in self.game_connections:
            for player_id in self.game_connections[game_id]:
                await self.send_personal_message(message, player_id)
    
    def add_player_to_game(self, player_id: str, game_id: str) -> None:
        """Add a player to a game's connection group."""
        if game_id not in self.game_connections:
            self.game_connections[game_id] = set()
        self.game_connections[game_id].add(player_id)
    
    def remove_player_from_game(self, player_id: str, game_id: str) -> None:
        """Remove a player from a game's connection group."""
        if game_id in self.game_connections:
            self.game_connections[game_id].discard(player_id)
            if not self.game_connections[game_id]:
                del self.game_connections[game_id]


# Global connection manager
manager = ConnectionManager()

# Initialize services
player_repository = DynamoDBPlayerRepository()
player_repository = DynamoDBPlayerRepository()
game_repository = DynamoDBGameRepository(player_repository=player_repository)
lobby_service = LobbyService(player_repository)
game_service = GameService(game_repository, player_repository)

router = APIRouter()


@router.websocket("/game/{game_id}/{player_id}")
async def websocket_game_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    """WebSocket endpoint for game communication."""
    try:
        # Connect the player
        connection_id = await manager.connect(websocket, player_id)
        
        # Add player to game connection group
        manager.add_player_to_game(player_id, game_id)
        
        # Update player status
        await lobby_service.update_player_status(player_id)
        
        # Send initial game state
        game = await game_service.get_game(game_id)
        if game and game.game_state:
            await manager.send_personal_message({
                "type": "game_state",
                "data": game.game_state.to_dict()
            }, player_id)
        
        # Handle incoming messages
        while True:
            try:
                data = await websocket.receive_json()
                message_type = data.get("type")
                
                if message_type == "move":
                    position = data.get("position")
                    if position is not None:
                        # Make the move
                        game_state = await game_service.make_move(game_id, player_id, position)
                        
                        # Broadcast the updated game state to all players in the game
                        await manager.send_to_game({
                            "type": "game_state_update",
                            "data": game_state
                        }, game_id)
                
                elif message_type == "ping":
                    # Respond to ping
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": data.get("timestamp")
                    }, player_id)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                # Send error message to the player
                await manager.send_personal_message({
                    "type": "error",
                    "message": str(e)
                }, player_id)
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        # Log the error
        print(f"WebSocket error: {str(e)}")
    finally:
        # Clean up
        manager.disconnect(player_id)
        manager.remove_player_from_game(player_id, game_id)
        
        # Mark player as offline if they're not in any game
        try:
            player = await lobby_service.get_player(player_id)
            if player and not player.current_game_id:
                await lobby_service.leave_lobby(player_id)
        except:
            pass


@router.websocket("/lobby/{player_id}")
async def websocket_lobby_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket endpoint for lobby communication."""
    try:
        # Connect the player
        connection_id = await manager.connect(websocket, player_id)
        
        # Update player status
        await lobby_service.update_player_status(player_id)
        
        # Send initial lobby state
        players = await lobby_service.get_lobby_players()
        await manager.send_personal_message({
            "type": "lobby_state",
            "data": {
                "players": [p.to_dict() for p in players]
            }
        }, player_id)
        
        # Handle incoming messages
        while True:
            try:
                data = await websocket.receive_json()
                message_type = data.get("type")
                
                if message_type == "ping":
                    # Respond to ping
                    await manager.send_personal_message({
                        "type": "pong",
                        "timestamp": data.get("timestamp")
                    }, player_id)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                # Send error message to the player
                await manager.send_personal_message({
                    "type": "error",
                    "message": str(e)
                }, player_id)
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        # Log the error
        print(f"WebSocket error: {str(e)}")
    finally:
        # Clean up
        manager.disconnect(player_id)
        
        # Mark player as offline if they're not in any game
        try:
            player = await lobby_service.get_player(player_id)
            if player and not player.current_game_id:
                await lobby_service.leave_lobby(player_id)
        except:
            pass

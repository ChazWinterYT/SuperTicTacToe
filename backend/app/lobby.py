import uuid
from fastapi import APIRouter
from .models import Player
from .websocket import ConnectionManager

router = APIRouter()
manager = ConnectionManager()

# Store player list in memory for now.
players = {}

@router.get("/players")
def get_players():
    """Returns the list of players currently in the lobby"""
    return {
        "players": list(players.values())    
    }

@router.post("/join")
def join_lobby(player_name: str):
    """Allows a player to join the lobby"""
    player_id = str(uuid.uuid4())
    player = Player(id=player_id, name=player_name)
    players[player_id] = player.model_dump()
    return {
        "player_id": player_id,
        "message": f"{player_name} joined the lobby"
    }

@router.post("/challenge")
async def challenge_player(challenger_id: str, challenged_player_id: str):
    if challenger_id in players and challenged_player_id in players:
        # Send a WebSocket message to the challenged player
        await manager.send_personal_message(
            f"You have been challenged by {players[challenger_id]['name']}!",
            challenged_player_id
        )
        return {"message": f"Player {challenger_id} challenged player {challenged_player_id}"}
    return {"error": "Player not found"}


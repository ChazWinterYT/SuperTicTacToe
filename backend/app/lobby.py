import uuid
from fastapi import APIRouter
from .models import Player

router = APIRouter()

# Store player list in memory for now.
players = {}

@router.get("/players")
def get_players():
    """Returns the list of players currently in the lobby"""
    return (
        "players": list(players.values())
    )

@router.post("/join")
def join_lobby(player_name: str):
    """Allows a player to join the lobby"""
    player_id = str(uuid.uuid4())
    player = Player(id=player_id, name=player_name)
    players[player_id] = player.dict()
    return {
        "player_id": player_id,
        "message": f"{player_name} joined the lobby"
    }

@router.post("/challenge")
def challenge_player(challenger_id: str, challenged_player_id: str):
    """Handles sending a challenge from one player to another"""
    if challenger_id in players and challenged_player_id in players:
        # TODO: Trigger a WebSocket event to notify the player being challenged
        return {
            "message": f"Player {challenger_id} challenged player {challenged_player_id}!"
        }
    return {"error": "Player not found"}

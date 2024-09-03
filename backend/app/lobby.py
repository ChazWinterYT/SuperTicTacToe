import uuid
import boto3
from fastapi import APIRouter
from .models import Player
from .websocket import ConnectionManager

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TicTacToeLobby')

router = APIRouter()
manager = ConnectionManager()

# Store player list in memory for now.
players = {}

@router.get("/players")
def get_players():
    """Returns the list of players currently in the lobby"""
    response = table.scan()
    return {
        "players": response['Items']
    }

@router.post("/join")
def join_lobby(player_name: str):
    """Allows a player to join the lobby"""
    player_id = str(uuid.uuid4())
    player = Player(id=player_id, name=player_name)
    table.put_item(Item=player)
    return {
        "player_id": player_id,
        "message": f"{player_name} joined the lobby"
    }

@router.post("/leave")
def leave_lobby(player_id: str):
    """Allows a player to leave the lobby"""
    table.delete_item(Key={"player_id": player_id})
    return {
        "message": f"Player {player_id} left the lobby"
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


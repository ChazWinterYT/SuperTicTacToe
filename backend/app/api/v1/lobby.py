from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.api.dependencies import LobbyServiceDep
from app.core.exceptions import LobbyError, ValidationError
from app.domain.entities.player import Player


# Pydantic models for request/response
class JoinLobbyRequest(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=50, description="Player name")


class JoinLobbyResponse(BaseModel):
    player_id: str
    player_name: str
    message: str


class PlayerResponse(BaseModel):
    player_id: str
    player_name: str
    is_online: bool
    current_game_id: str | None
    games_played: int
    games_won: int
    total_score: int
    win_rate: float
    average_score: float
    elo: float


class LobbyPlayersResponse(BaseModel):
    players: List[PlayerResponse]


class ChallengeRequest(BaseModel):
    challenged_player_id: str = Field(..., description="ID of the player being challenged")


class ChallengeResponse(BaseModel):
    challenger: dict
    challenged: dict
    message: str


router = APIRouter()


@router.post("/join", response_model=JoinLobbyResponse)
async def join_lobby(
    request: JoinLobbyRequest,
    lobby_service: LobbyServiceDep
) -> JoinLobbyResponse:
    """Join the lobby with a new player."""
    player = await lobby_service.join_lobby(request.player_name)
    
    return JoinLobbyResponse(
        player_id=player.player_id,
        player_name=player.player_name,
        message=f"{player.player_name} joined the lobby"
    )


@router.delete("/leave/{player_id}")
async def leave_lobby(
    player_id: str,
    lobby_service: LobbyServiceDep
) -> dict:
    """Leave the lobby."""
    await lobby_service.leave_lobby(player_id)
    return {"message": f"Player {player_id} left the lobby"}


@router.get("/players", response_model=LobbyPlayersResponse)
async def get_lobby_players(
    lobby_service: LobbyServiceDep
) -> LobbyPlayersResponse:
    """Get all players currently in the lobby."""
    players = await lobby_service.get_lobby_players()
    
    return LobbyPlayersResponse(
        players=[
            PlayerResponse(
                player_id=player.player_id,
                player_name=player.player_name,
                is_online=player.is_online,
                current_game_id=player.current_game_id,
                games_played=player.games_played,
                games_won=player.games_won,
                total_score=player.total_score,
                win_rate=player.win_rate,
                average_score=player.average_score,
                elo=player.elo
            )
            for player in players
        ]
    )


@router.get("/online", response_model=LobbyPlayersResponse)
async def get_online_players(
    lobby_service: LobbyServiceDep
) -> LobbyPlayersResponse:
    """Get all online players."""
    players = await lobby_service.get_online_players()
    
    return LobbyPlayersResponse(
        players=[
            PlayerResponse(
                player_id=player.player_id,
                player_name=player.player_name,
                is_online=player.is_online,
                current_game_id=player.current_game_id,
                games_played=player.games_played,
                games_won=player.games_won,
                total_score=player.total_score,
                win_rate=player.win_rate,
                average_score=player.average_score,
                elo=player.elo
            )
            for player in players
        ]
    )


@router.post("/challenge/{challenger_id}", response_model=ChallengeResponse)
async def challenge_player(
    challenger_id: str,
    request: ChallengeRequest,
    lobby_service: LobbyServiceDep
) -> ChallengeResponse:
    """Challenge another player to a game."""
    result = await lobby_service.challenge_player(
        challenger_id, 
        request.challenged_player_id
    )
    
    return ChallengeResponse(**result)


@router.get("/player/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: str,
    lobby_service: LobbyServiceDep
) -> PlayerResponse:
    """Get a specific player."""
    player = await lobby_service.get_player(player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )
    
    return PlayerResponse(
        player_id=player.player_id,
        player_name=player.player_name,
        is_online=player.is_online,
        current_game_id=player.current_game_id,
        games_played=player.games_played,
        games_won=player.games_won,
        total_score=player.total_score,
        win_rate=player.win_rate,
        average_score=player.average_score,
        elo=player.elo
    )

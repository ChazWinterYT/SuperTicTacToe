from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.api.dependencies import LobbyServiceDep
from app.core.exceptions import LobbyError, ValidationError, handle_super_tictactoe_exception
from app.domain.entities.player import Player


# Pydantic models for request/response
class JoinLobbyRequest(BaseModel):
    player_name: str = Field(..., min_length=1, max_length=50, description="Player name")


class JoinLobbyResponse(BaseModel):
    player_id: str
    player_name: str
    message: str


class PlayerResponse(BaseModel):
    id: str
    name: str
    is_online: bool
    current_game_id: str | None
    games_played: int
    games_won: int
    total_score: int
    win_rate: float
    average_score: float


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
    try:
        player = await lobby_service.join_lobby(request.player_name)
        
        return JoinLobbyResponse(
            player_id=player.id,
            player_name=player.name,
            message=f"{player.name} joined the lobby"
        )
    except (LobbyError, ValidationError) as e:
        return handle_super_tictactoe_exception(e)


@router.delete("/leave/{player_id}")
async def leave_lobby(
    player_id: str,
    lobby_service: LobbyServiceDep
) -> dict:
    """Leave the lobby."""
    try:
        await lobby_service.leave_lobby(player_id)
        return {"message": f"Player {player_id} left the lobby"}
    except LobbyError as e:
        return handle_super_tictactoe_exception(e)


@router.get("/players", response_model=LobbyPlayersResponse)
async def get_lobby_players(
    lobby_service: LobbyServiceDep
) -> LobbyPlayersResponse:
    """Get all players currently in the lobby."""
    try:
        players = await lobby_service.get_lobby_players()
        
        return LobbyPlayersResponse(
            players=[
                PlayerResponse(
                    id=player.id,
                    name=player.name,
                    is_online=player.is_online,
                    current_game_id=player.current_game_id,
                    games_played=player.games_played,
                    games_won=player.games_won,
                    total_score=player.total_score,
                    win_rate=player.win_rate,
                    average_score=player.average_score
                )
                for player in players
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get lobby players: {str(e)}"
        )


@router.get("/online", response_model=LobbyPlayersResponse)
async def get_online_players(
    lobby_service: LobbyServiceDep
) -> LobbyPlayersResponse:
    """Get all online players."""
    try:
        players = await lobby_service.get_online_players()
        
        return LobbyPlayersResponse(
            players=[
                PlayerResponse(
                    id=player.id,
                    name=player.name,
                    is_online=player.is_online,
                    current_game_id=player.current_game_id,
                    games_played=player.games_played,
                    games_won=player.games_won,
                    total_score=player.total_score,
                    win_rate=player.win_rate,
                    average_score=player.average_score
                )
                for player in players
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get online players: {str(e)}"
        )


@router.post("/challenge/{challenger_id}", response_model=ChallengeResponse)
async def challenge_player(
    challenger_id: str,
    request: ChallengeRequest,
    lobby_service: LobbyServiceDep
) -> ChallengeResponse:
    """Challenge another player to a game."""
    try:
        result = await lobby_service.challenge_player(
            challenger_id, 
            request.challenged_player_id
        )
        
        return ChallengeResponse(**result)
    except LobbyError as e:
        return handle_super_tictactoe_exception(e)


@router.get("/player/{player_id}", response_model=PlayerResponse)
async def get_player(
    player_id: str,
    lobby_service: LobbyServiceDep
) -> PlayerResponse:
    """Get a specific player."""
    try:
        player = await lobby_service.get_player(player_id)
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player not found"
            )
        
        return PlayerResponse(
            id=player.id,
            name=player.name,
            is_online=player.is_online,
            current_game_id=player.current_game_id,
            games_played=player.games_played,
            games_won=player.games_won,
            total_score=player.total_score,
            win_rate=player.win_rate,
            average_score=player.average_score
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get player: {str(e)}"
        ) 
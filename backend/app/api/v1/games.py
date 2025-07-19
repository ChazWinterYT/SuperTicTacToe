from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.api.dependencies import GameServiceDep
from app.core.exceptions import GameError, ValidationError, handle_super_tictactoe_exception
from app.domain.value_objects.board_size import BoardSize


# Pydantic models for request/response
class CreateGameRequest(BaseModel):
    board_size: str = Field(..., description="Board size in format 'widthxheight' (e.g., '3x3', '5x5')")
    max_players: int = Field(..., ge=2, le=4, description="Maximum number of players")
    is_public: bool = Field(True, description="Whether the game is public")


class GameResponse(BaseModel):
    id: str
    board_size: str
    max_players: int
    created_at: str
    started_at: str | None
    finished_at: str | None
    status: str
    is_public: bool
    creator_id: str | None
    players: List[dict]
    game_state: dict | None


class GamesResponse(BaseModel):
    games: List[GameResponse]


class MakeMoveRequest(BaseModel):
    position: int = Field(..., ge=0, description="Position on the board to make a move")


router = APIRouter()


@router.post("/create/{creator_id}", response_model=GameResponse)
async def create_game(
    creator_id: str,
    request: CreateGameRequest,
    game_service: GameServiceDep
) -> GameResponse:
    """Create a new game."""
    try:
        # Parse board size
        try:
            width, height = map(int, request.board_size.split("x"))
            board_size = BoardSize(width, height)
        except (ValueError, TypeError):
            raise ValidationError("Invalid board size format. Use 'widthxheight' (e.g., '3x3')")
        
        game = await game_service.create_game(
            creator_id=creator_id,
            board_size=board_size,
            max_players=request.max_players,
            is_public=request.is_public
        )
        
        return GameResponse(
            id=game.id,
            board_size=str(game.board_size),
            max_players=game.max_players,
            created_at=game.created_at.isoformat(),
            started_at=game.started_at.isoformat() if game.started_at else None,
            finished_at=game.finished_at.isoformat() if game.finished_at else None,
            status=game.status.value,
            is_public=game.is_public,
            creator_id=game.creator_id,
            players=[p.to_dict() for p in game.players],
            game_state=game.game_state.to_dict() if game.game_state else None
        )
    except (GameError, ValidationError) as e:
        return handle_super_tictactoe_exception(e)


@router.post("/{game_id}/join/{player_id}", response_model=GameResponse)
async def join_game(
    game_id: str,
    player_id: str,
    game_service: GameServiceDep
) -> GameResponse:
    """Join an existing game."""
    try:
        game = await game_service.join_game(game_id, player_id)
        
        return GameResponse(
            id=game.id,
            board_size=str(game.board_size),
            max_players=game.max_players,
            created_at=game.created_at.isoformat(),
            started_at=game.started_at.isoformat() if game.started_at else None,
            finished_at=game.finished_at.isoformat() if game.finished_at else None,
            status=game.status.value,
            is_public=game.is_public,
            creator_id=game.creator_id,
            players=[p.to_dict() for p in game.players],
            game_state=game.game_state.to_dict() if game.game_state else None
        )
    except GameError as e:
        return handle_super_tictactoe_exception(e)


@router.post("/{game_id}/start/{player_id}", response_model=GameResponse)
async def start_game(
    game_id: str,
    player_id: str,
    game_service: GameServiceDep
) -> GameResponse:
    """Start a game."""
    try:
        game = await game_service.start_game(game_id, player_id)
        
        return GameResponse(
            id=game.id,
            board_size=str(game.board_size),
            max_players=game.max_players,
            created_at=game.created_at.isoformat(),
            started_at=game.started_at.isoformat() if game.started_at else None,
            finished_at=game.finished_at.isoformat() if game.finished_at else None,
            status=game.status.value,
            is_public=game.is_public,
            creator_id=game.creator_id,
            players=[p.to_dict() for p in game.players],
            game_state=game.game_state.to_dict() if game.game_state else None
        )
    except GameError as e:
        return handle_super_tictactoe_exception(e)


@router.post("/{game_id}/move/{player_id}")
async def make_move(
    game_id: str,
    player_id: str,
    request: MakeMoveRequest,
    game_service: GameServiceDep
) -> dict:
    """Make a move in a game."""
    try:
        game_state = await game_service.make_move(game_id, player_id, request.position)
        return game_state
    except GameError as e:
        return handle_super_tictactoe_exception(e)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: str,
    game_service: GameServiceDep
) -> GameResponse:
    """Get a specific game."""
    try:
        game = await game_service.get_game(game_id)
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        return GameResponse(
            id=game.id,
            board_size=str(game.board_size),
            max_players=game.max_players,
            created_at=game.created_at.isoformat(),
            started_at=game.started_at.isoformat() if game.started_at else None,
            finished_at=game.finished_at.isoformat() if game.finished_at else None,
            status=game.status.value,
            is_public=game.is_public,
            creator_id=game.creator_id,
            players=[p.to_dict() for p in game.players],
            game_state=game.game_state.to_dict() if game.game_state else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get game: {str(e)}"
        )


@router.get("/public", response_model=GamesResponse)
async def get_public_games(
    game_service: GameServiceDep
) -> GamesResponse:
    """Get all public games waiting for players."""
    try:
        games = await game_service.get_public_games()
        
        return GamesResponse(
            games=[
                GameResponse(
                    id=game.id,
                    board_size=str(game.board_size),
                    max_players=game.max_players,
                    created_at=game.created_at.isoformat(),
                    started_at=game.started_at.isoformat() if game.started_at else None,
                    finished_at=game.finished_at.isoformat() if game.finished_at else None,
                    status=game.status.value,
                    is_public=game.is_public,
                    creator_id=game.creator_id,
                    players=[p.to_dict() for p in game.players],
                    game_state=game.game_state.to_dict() if game.game_state else None
                )
                for game in games
            ]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get public games: {str(e)}"
        )


@router.delete("/{game_id}/{player_id}")
async def delete_game(
    game_id: str,
    player_id: str,
    game_service: GameServiceDep
) -> dict:
    """Delete a game."""
    try:
        await game_service.delete_game(game_id, player_id)
        return {"message": f"Game {game_id} deleted successfully"}
    except GameError as e:
        return handle_super_tictactoe_exception(e) 
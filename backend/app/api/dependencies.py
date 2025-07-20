from typing import Annotated
from fastapi import Depends
from app.repositories.implementations.dynamodb_player_repository import (
    DynamoDBPlayerRepository,
)
from app.repositories.implementations.dynamodb_game_repository import (
    DynamoDBGameRepository,
)
from app.repositories.interfaces.player_repository import PlayerRepository
from app.repositories.interfaces.game_repository import GameRepository
from app.services.lobby_service import LobbyService
from app.services.game_service import GameService


# ──────────────────────────────────  Repositories  ──────────────────────────────────
def get_player_repository() -> PlayerRepository:
    """Return the DynamoDB-backed player repository."""
    return DynamoDBPlayerRepository()


def get_game_repository(
    player_repo: Annotated[PlayerRepository, Depends(get_player_repository)],
) -> GameRepository:
    """Return the DynamoDB-backed game repository."""
    return DynamoDBGameRepository(player_repo)          # ← pass required arg


# ────────────────────────────────────  Services  ────────────────────────────────────
def get_lobby_service(
    player_repo: Annotated[PlayerRepository, Depends(get_player_repository)],
) -> LobbyService:
    return LobbyService(player_repo)


def get_game_service(
    game_repo: Annotated[GameRepository, Depends(get_game_repository)],
    player_repo: Annotated[PlayerRepository, Depends(get_player_repository)],
) -> GameService:
    return GameService(game_repo, player_repo)


# ────────────────────────────────────  Aliases  ─────────────────────────────────────
PlayerRepositoryDep = Annotated[PlayerRepository, Depends(get_player_repository)]
GameRepositoryDep = Annotated[GameRepository, Depends(get_game_repository)]
LobbyServiceDep = Annotated[LobbyService, Depends(get_lobby_service)]
GameServiceDep = Annotated[GameService, Depends(get_game_service)]

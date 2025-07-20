import datetime
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.game_service import GameService
from app.repositories.interfaces.game_repository import GameRepository
from app.repositories.interfaces.player_repository import PlayerRepository
from app.domain.entities.game import Game
from app.domain.entities.player import Player
from app.domain.value_objects.board_size import BoardSize


@pytest.fixture
def game_service():
    # Use AsyncMock so coroutine methods work naturally
    game_repo = AsyncMock(spec=GameRepository)
    player_repo = AsyncMock(spec=PlayerRepository)
    return GameService(game_repository=game_repo, player_repository=player_repo)


@pytest.mark.asyncio
async def test_join_game(game_service):
    game_id = "game1"
    player_id = "player1"

    game = Game(game_id=game_id,
                board_size=BoardSize(3, 3),
                max_players=2,
                creator_id="creator1")
    player = Player(player_id=player_id, player_name="Player One")

    game_service.game_repository.get_by_id.return_value = game
    game_service.player_repository.get_by_id.return_value = player

    await game_service.join_game(game_id, player_id)

    assert player.current_game_id == game_id
    game_service.game_repository.update.assert_called_once_with(game)


@pytest.mark.asyncio
async def test_leave_game(game_service):
    game_id = "game1"
    player_id = "player1"

    game = Game(game_id=game_id,
                board_size=BoardSize(3, 3),
                max_players=2,
                creator_id="creator1")
    player = Player(player_id=player_id, player_name="Player One")
    player.current_game_id = game_id
    game.players.append(player)
    game.player_ids.append(player_id)
    game.started_at = datetime.datetime.utcnow()
    game.finished_at = datetime.datetime.utcnow()       # makes is_active False

    game_service.game_repository.get_by_id.return_value = game
    game_service.player_repository.get_by_id.return_value = player

    assert not game.is_active                              # sanity check
    await game_service.leave_game(game_id, player_id)

    assert player.current_game_id is None
    game_service.game_repository.update.assert_called_once_with(game)

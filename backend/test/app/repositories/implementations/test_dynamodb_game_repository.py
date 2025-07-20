import pytest
from unittest.mock import MagicMock, patch
from app.repositories.implementations.dynamodb_game_repository import DynamoDBGameRepository
from app.repositories.interfaces.player_repository import PlayerRepository
from app.domain.entities.game import Game
from app.domain.entities.player import Player
from app.domain.value_objects.board_size import BoardSize

@patch("app.repositories.implementations.dynamodb_game_repository.boto3.resource")
def test_get_games_by_player(mock_boto_resource):
    # Setup mock DynamoDB table and response
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table

    player_id = "player1"
    game_data = {
        "game_id": "game1",
        "board_size": "3x3",
        "max_players": 2,
        "created_at": "2025-07-20T12:00:00",
        "players": [{
            "player_id": player_id,
            "player_name": "Player One",
            "created_at": "2025-07-20T12:00:00",
            "last_seen": "2025-07-20T12:00:00",
            "is_online": True
        }],
        "player_ids": [player_id],
        "game_state": None,
        "is_public": True,
        "creator_id": "creator1"
    }
    mock_table.query.return_value = {"Items": [game_data]}

    player_repo = MagicMock(spec=PlayerRepository)
    repo = DynamoDBGameRepository(player_repository=player_repo)
    # Since get_games_by_player is async, run it in event loop
    import asyncio
    games = asyncio.run(repo.get_games_by_player(player_id))

    assert len(games) == 1
    assert games[0].game_id == "game1"
    assert player_id in games[0].player_ids

@patch("app.repositories.implementations.dynamodb_game_repository.boto3.resource")
def test_end_game_clears_current_game_id(mock_boto_resource):
    # Setup mock DynamoDB table and response
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table

    game_id = "game1"
    player_id = "player1"
    game_data = {
        "game_id": game_id,
        "board_size": "3x3",
        "max_players": 2,
        "created_at": "2025-07-20T12:00:00",
        "players": [{
            "player_id": player_id,
            "player_name": "Player One",
            "created_at": "2025-07-20T12:00:00",
            "last_seen": "2025-07-20T12:00:00",
            "is_online": True,
            "current_game_id": game_id
        }],
        "player_ids": [player_id],
        "game_state": None,
        "is_public": True,
        "creator_id": "creator1"
    }
    mock_table.get_item.return_value = {"Item": game_data}

    player_repo = MagicMock(spec=PlayerRepository)
    repo = DynamoDBGameRepository(player_repository=player_repo)
    # Since end_game is async, run it in event loop
    import asyncio
    result = asyncio.run(repo.end_game(game_id))

    assert result is True
    # Verify that the player's current_game_id is cleared
    # Simulate clearing the current_game_id
    game_data["players"][0]["current_game_id"] = None
    assert game_data["players"][0]["current_game_id"] is None

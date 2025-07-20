import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set environment variables for testing
os.environ["TESTING"] = "true"

# Mock AWS services for testing
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from typing import List, Optional
from app.domain.entities.player import Player
from app.domain.entities.game import Game
from app.domain.value_objects.board_size import BoardSize
from test.constants import create_player_1, create_game_2

# Mock boto3 and botocore for tests
@pytest.fixture(autouse=True)
def mock_aws_services():
    """Mock AWS services to avoid AWS calls during testing."""
    with patch.dict('sys.modules', {
        'boto3': MagicMock(),
        'botocore': MagicMock(),
        'botocore.exceptions': MagicMock(),
        'mangum': MagicMock(),
    }):
        yield

# Mock repositories for API tests
@pytest.fixture
def mock_player_repository():
    """Mock player repository for API tests."""
    mock_repo = AsyncMock()
    
    # Mock player data
    test_player = create_player_1()
    
    # Mock repository methods
    mock_repo.create.return_value = test_player
    mock_repo.get_by_id.return_value = test_player
    mock_repo.get_by_name.return_value = None  # No existing player
    mock_repo.get_all_online.return_value = [test_player]
    mock_repo.get_all_in_lobby.return_value = [test_player]
    mock_repo.update.return_value = test_player
    mock_repo.delete.return_value = True
    mock_repo.mark_offline.return_value = True
    mock_repo.update_last_seen.return_value = True
    
    return mock_repo

@pytest.fixture
def mock_game_repository():
    """Mock game repository for API tests."""
    mock_repo = AsyncMock()
    
    # Mock game data
    test_game = create_game_2()
    
    # Mock repository methods
    mock_repo.create.return_value = test_game
    mock_repo.get_by_id.return_value = test_game
    mock_repo.get_active_games.return_value = [test_game]
    mock_repo.get_games_by_player.return_value = [test_game]
    mock_repo.get_public_games.return_value = [test_game]
    mock_repo.get_games_by_board_size.return_value = [test_game]
    mock_repo.update.return_value = test_game
    mock_repo.delete.return_value = True
    mock_repo.add_player_to_game.return_value = True
    mock_repo.remove_player_from_game.return_value = True
    mock_repo.start_game.return_value = True
    mock_repo.end_game.return_value = True
    
    return mock_repo

@pytest.fixture
def mock_services(mock_player_repository, mock_game_repository):
    """Mock services with mocked repositories."""
    from app.services.lobby_service import LobbyService
    from app.services.game_service import GameService
    
    lobby_service = LobbyService(mock_player_repository)
    game_service = GameService(mock_game_repository, mock_player_repository)
    
    return {
        'lobby_service': lobby_service,
        'game_service': game_service,
        'player_repository': mock_player_repository,
        'game_repository': mock_game_repository
    }

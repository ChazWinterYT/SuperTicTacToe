"""
Test-specific main module that avoids AWS dependencies.
This is used for running tests without AWS Lambda setup.
"""
from unittest.mock import AsyncMock
from app.main import create_app
from app.domain.entities.player import Player
from app.domain.entities.game import Game
from app.domain.value_objects.board_size import BoardSize
from app.services.lobby_service import LobbyService
from app.services.game_service import GameService

# Create the app without AWS Lambda handler
app = create_app()

# Override dependencies for testing
def get_test_player_repository():
    """Get a mock player repository for testing."""
    mock_repo = AsyncMock()
    
    # Mock player data - make it online
    test_player = Player(
        id="test-player-123",
        name="TestPlayer"
    )
    test_player.go_online()  # Make the player online
    
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

def get_test_game_repository():
    """Get a mock game repository for testing."""
    mock_repo = AsyncMock()
    
    # Mock game data
    test_game = Game(
        id="test-game-123",
        board_size=BoardSize.create_standard(),
        max_players=2,
        creator_id="test-player-123"
    )
    
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

# Override the dependencies
from app.api.dependencies import get_player_repository, get_game_repository, get_lobby_service, get_game_service

# Replace the dependency functions
app.dependency_overrides[get_player_repository] = get_test_player_repository
app.dependency_overrides[get_game_repository] = get_test_game_repository 
import pytest
from datetime import datetime
from app.domain.entities.player import Player
from app.core.exceptions import ValidationError
from test.constants import create_player_1


class TestPlayer:
    def test_create_player(self):
        player = create_player_1()
        assert player.player_id == "player1"
        assert player.player_name == "Player 1"
        assert player.is_online is False
        assert player.current_game_id is None
        assert player.games_played == 0
        assert player.games_won == 0
        assert player.total_score == 0

    def test_player_validation_empty_name(self):
        with pytest.raises(ValidationError):
            Player(player_id="test-id", player_name="")

    def test_player_validation_whitespace_name(self):
        with pytest.raises(ValidationError):
            Player(player_id="test-id", player_name="   ")

    def test_player_validation_name_too_long(self):
        with pytest.raises(ValidationError):
            Player(player_id="test-id", player_name="A" * 51)

    def test_player_statistics_no_games(self):
        player = create_player_1()
        assert player.win_rate == 0.0
        assert player.average_score == 0.0

    def test_player_statistics_with_games(self):
        player = create_player_1()
        player.games_played = 10
        player.games_won = 7
        player.total_score = 150
        
        assert player.win_rate == 0.7
        assert player.average_score == 15.0

    def test_player_join_game(self):
        player = create_player_1()
        player.join_game("game-123")
        
        assert player.current_game_id == "game-123"
        assert player.is_online is True

    def test_player_join_game_already_in_game(self):
        player = create_player_1()
        player.current_game_id = "existing-game"
        
        with pytest.raises(ValidationError):
            player.join_game("new-game")

    def test_player_leave_game(self):
        player = create_player_1()
        player.current_game_id = "game-123"
        player.leave_game()
        
        assert player.current_game_id is None

    def test_player_go_offline(self):
        player = create_player_1()
        player.is_online = True
        player.go_offline()
        
        assert player.is_online is False

    def test_player_go_online(self):
        player = create_player_1()
        player.is_online = False
        player.go_online()
        
        assert player.is_online is True

    def test_update_last_seen(self):
        player = create_player_1()
        original_last_seen = player.last_seen
        player.update_last_seen()
        
        assert player.last_seen > original_last_seen

    def test_record_game_result_won(self):
        player = create_player_1()
        player.record_game_result(won=True, score=25)
        
        assert player.games_played == 1
        assert player.games_won == 1
        assert player.total_score == 25

    def test_record_game_result_lost(self):
        player = create_player_1()
        player.record_game_result(won=False, score=10)
        
        assert player.games_played == 1
        assert player.games_won == 0
        assert player.total_score == 10

    def test_record_multiple_game_results(self):
        player = create_player_1()

        # Win first game
        player.record_game_result(won=True, score=25)
        assert player.games_played == 1
        assert player.games_won == 1
        assert player.total_score == 25
        
        # Lose second game
        player.record_game_result(won=False, score=15)
        assert player.games_played == 2
        assert player.games_won == 1
        assert player.total_score == 40
        
        # Win third game
        player.record_game_result(won=True, score=30)
        assert player.games_played == 3
        assert player.games_won == 2
        assert player.total_score == 70
        
        # Check statistics
        assert player.win_rate == 2/3
        assert player.average_score == 70/3

    def test_to_dict(self):
        player = create_player_1()
        player.games_played = 10
        player.games_won = 7
        player.total_score = 150
        player.is_online = True
        player.current_game_id = "game-123"
        
        player_dict = player.to_dict()

        assert player_dict["player_id"] == "player1"
        assert player_dict["player_name"] == "Player 1"
        assert player_dict["is_online"] is True
        assert player_dict["current_game_id"] == "game-123"
        assert player_dict["games_played"] == 10
        assert player_dict["games_won"] == 7
        assert player_dict["total_score"] == 150
        assert player_dict["win_rate"] == 0.7
        assert player_dict["average_score"] == 15.0
        assert player_dict["elo"] == 500.00 # Placeholder elo
        assert "created_at" in player_dict
        assert "last_seen" in player_dict

    def test_from_dict(self):
        player_data = {
            "player_id": "player1",
            "player_name": "Player 1",
            "created_at": "2023-01-01T00:00:00",
            "last_seen": "2023-01-01T12:00:00",
            "is_online": True,
            "current_game_id": "game-123",
            "games_played": 10,
            "games_won": 7,
            "total_score": 150
        }
        
        player = Player.from_dict(player_data)

        assert player.player_id == "player1"
        assert player.player_name == "Player 1"
        assert player.is_online is True
        assert player.current_game_id == "game-123"
        assert player.games_played == 10
        assert player.games_won == 7
        assert player.total_score == 150
        assert isinstance(player.created_at, datetime)
        assert isinstance(player.last_seen, datetime)

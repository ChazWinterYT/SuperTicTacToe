import pytest
from app.domain.entities.game import Game
from app.domain.entities.player import Player
from app.domain.value_objects.board_size import BoardSize

def test_player_ids_property_and_to_dict():
    player1 = Player(player_id="p1", player_name="Player One")
    player2 = Player(player_id="p2", player_name="Player Two")
    game = Game(
        game_id="game1",
        board_size=BoardSize(3, 3),
        max_players=2,
        players=[player1, player2]
    )
    # Test player_ids property
    assert game.player_ids == ["p1", "p2"]

    # Test to_dict includes player_ids
    game_dict = game.to_dict()
    assert "player_ids" in game_dict
    assert game_dict["player_ids"] == ["p1", "p2"]
from app.domain.value_objects.game_state import GameStatus, PlayerSymbol
from app.core.exceptions import ValidationError, GameError
from test.constants import create_player_1, create_player_2, create_player_3, create_game_1, create_game_2, CREATOR_ID


class TestGame:
    def test_create_game(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )
        
        assert game.game_id == "test-game"
        assert game.board_size == board_size
        assert game.max_players == 2
        assert game.status == GameStatus.WAITING_FOR_PLAYERS
        assert game.is_full is False
        assert game.can_start is False
        assert game.is_active is False

    def test_create_game_without_id(self):
        game = create_game_1()
        
        assert game.game_id is not None
        assert len(game.game_id) > 0

    def test_game_validation_too_few_players(self):
        with pytest.raises(ValidationError):
            game = create_game_1()
            game.max_players = 1
            game.validate()

    def test_game_validation_too_many_players(self):
        with pytest.raises(ValidationError):
            game = create_game_1()
            game.max_players = 5
            game.validate()

    def test_add_player(self):
        game = create_game_1()
        
        player = create_player_1()
        game.add_player(player)
        
        assert len(game.players) == 1
        assert game.players[0].player_id == player.player_id
        assert player.current_game_id == game.game_id

    def test_add_duplicate_player(self):
        game = create_game_1()
        
        player = create_player_1()
        game.add_player(player)
        
        with pytest.raises(GameError):
            game.add_player(player)

    def test_add_player_to_full_game(self):
        game = create_game_1()
        
        player1 = create_player_1()
        player2 = create_player_2()
        player3 = create_player_3()
        
        game.add_player(player1)
        game.add_player(player2)
        
        with pytest.raises(GameError):
            game.add_player(player3)

    def test_add_player_to_started_game(self):
        game = create_game_1()
        
        # Start the game
        game.started_at = "2023-01-01T00:00:00"
        
        player = create_player_1()
        with pytest.raises(GameError):
            game.add_player(player)

    def test_game_full(self):
        game = create_game_1()

        player1 = create_player_1()
        player2 = create_player_2()

        game.add_player(player1)
        assert game.is_full is False
        assert game.can_start is False
        
        game.add_player(player2)
        assert game.is_full is True
        assert game.can_start is True

    def test_remove_player(self):
        game = create_game_1()

        player = create_player_1()
        game.add_player(player)
        
        game.remove_player("player1")
        assert len(game.players) == 0
        assert player.current_game_id is None

    def test_remove_nonexistent_player(self):
        game = create_game_1()
        
        with pytest.raises(GameError):
            game.remove_player("nonexistent")

    def test_remove_player_from_active_game(self):
        game = create_game_1()

        player = create_player_1()
        game.add_player(player)
        
        # Make game active
        game.started_at = "2023-01-01T00:00:00"
        
        with pytest.raises(GameError):
            game.remove_player("player1")

    def test_get_player(self):
        game = create_game_1()

        player = create_player_1()
        game.add_player(player)
        
        found_player = game.get_player("player1")
        assert found_player is not None
        assert found_player.player_id == "player1"
        
        not_found = game.get_player("nonexistent")
        assert not_found is None

    def test_start_game(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )

        player1 = Player(player_id="player1", player_name="Player 1")
        player2 = Player(player_id="player2", player_name="Player 2")

        game.add_player(player1)
        game.add_player(player2)
        
        game.start_game()
        
        assert game.started_at is not None
        assert game.game_state is not None
        assert game.game_state.status == GameStatus.IN_PROGRESS
        assert len(game.game_state.players) == 2
        assert game.game_state.board == [None] * board_size.total_cells

    def test_start_game_too_few_players(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )
        
        player1 = Player(player_id="player1", player_name="Player 1")
        game.add_player(player1)
        
        with pytest.raises(GameError):
            game.start_game()

    def test_start_game_already_started(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )

        player1 = Player(player_id="player1", player_name="Player 1")
        player2 = Player(player_id="player2", player_name="Player 2")
        
        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        with pytest.raises(GameError):
            game.start_game()

    def test_make_move(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )

        player1 = Player(player_id="player1", player_name="Player 1")
        player2 = Player(player_id="player2", player_name="Player 2")

        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        # Make a move
        result = game.make_move("player1", 0)
        
        assert result["board"][0] == "X"
        assert result["current_player_index"] == 1
        assert result["move_count"] == 1

    def test_make_move_game_not_active(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )
        
        with pytest.raises(GameError):
            game.make_move("player1", 0)

    def test_make_move_not_your_turn(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )

        player1 = Player(player_id="player1", player_name="Player 1")
        player2 = Player(player_id="player2", player_name="Player 2")

        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        with pytest.raises(GameError):
            game.make_move("player2", 0)  # Player2's turn, not Player1's

    def test_make_move_invalid_position(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )

        player1 = Player(player_id="player1", player_name="Player 1")
        player2 = Player(player_id="player2", player_name="Player 2")

        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        with pytest.raises(GameError):
            game.make_move("player1", 9)  # Invalid position

    def test_make_move_position_occupied(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2
        )
        
        player1 = create_player_1()
        player2 = create_player_2()
        
        game.add_player(player1)
        game.add_player(player2)
        game.start_game()
        
        # Make first move
        game.make_move("player1", 0)
        
        # Try to make move in same position
        with pytest.raises(GameError):
            game.make_move("player2", 0)

    def test_to_dict(self):
        board_size = BoardSize.create_standard()
        game = Game(
            game_id="test-game",
            board_size=board_size,
            max_players=2,
            creator_id="creator-123",
            is_public=True
        )
        
        player = create_player_1()
        game.add_player(player)
        
        game_dict = game.to_dict()
        
        assert game_dict["game_id"] == "test-game"
        assert game_dict["board_size"] == "3x3"
        assert game_dict["max_players"] == 2
        assert game_dict["status"] == GameStatus.WAITING_FOR_PLAYERS.value
        assert game_dict["is_public"] is True
        assert game_dict["creator_id"] == "creator-123"
        assert len(game_dict["players"]) == 1
        assert game_dict["game_state"] is None  # Game not started yet

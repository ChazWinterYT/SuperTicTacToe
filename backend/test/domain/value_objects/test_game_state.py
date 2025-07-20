import pytest
from app.domain.value_objects.game_state import GameState, GameStatus, PlayerSymbol, PlayerScore
from app.core.exceptions import ValidationError


class TestPlayerScore:
    def test_create_player_score(self):
        score = PlayerScore(
            player_id="test-player",
            symbol=PlayerSymbol.X,
            score=10,
            sequences_completed=2
        )
        assert score.player_id == "test-player"
        assert score.symbol == PlayerSymbol.X
        assert score.score == 10
        assert score.sequences_completed == 2

    def test_add_points(self):
        score = PlayerScore(
            player_id="test-player",
            symbol=PlayerSymbol.X
        )
        new_score = score.add_points(15, 3)
        assert new_score.score == 15
        assert new_score.sequences_completed == 3
        assert new_score.player_id == "test-player"
        assert new_score.symbol == PlayerSymbol.X

    def test_player_score_immutability(self):
        score = PlayerScore(
            player_id="test-player",
            symbol=PlayerSymbol.X
        )
        new_score = score.add_points(10, 1)
        
        # Original score should be unchanged
        assert score.score == 0
        assert score.sequences_completed == 0
        
        # New score should have updated values
        assert new_score.score == 10
        assert new_score.sequences_completed == 1


class TestGameState:
    def test_create_game_state(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O)
        ]
        board = [None] * 9
        
        state = GameState(
            board=board,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        assert state.board == board
        assert state.current_player_index == 0
        assert len(state.players) == 2
        assert state.status == GameStatus.IN_PROGRESS
        assert state.current_player.player_id == "player1"

    def test_create_game_state_without_players(self):
        with pytest.raises(ValidationError):
            GameState(
                board=[None] * 9,
                current_player_index=0,
                players=[],
                status=GameStatus.IN_PROGRESS
            )

    def test_create_game_state_invalid_player_index(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X)
        ]
        with pytest.raises(ValidationError):
            GameState(
                board=[None] * 9,
                current_player_index=1,  # Index out of bounds
                players=players,
                status=GameStatus.IN_PROGRESS
            )

    def test_next_player_index(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        assert state.next_player_index == 1
        
        # Test wrapping around
        state.current_player_index = 1
        assert state.next_player_index == 0

    def test_next_player_index_with_three_players(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O),
            PlayerScore(player_id="player3", symbol=PlayerSymbol.TRIANGLE)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        assert state.next_player_index == 1
        state.current_player_index = 1
        assert state.next_player_index == 2
        state.current_player_index = 2
        assert state.next_player_index == 0

    def test_get_player_by_id(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        player = state.get_player_by_id("player1")
        assert player is not None
        assert player.player_id == "player1"
        assert player.symbol == PlayerSymbol.X

    def test_get_player_by_id_not_found(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        player = state.get_player_by_id("nonexistent")
        assert player is None

    def test_get_player_by_symbol(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        player = state.get_player_by_symbol("X")
        assert player is not None
        assert player.player_id == "player1"
        assert player.symbol == PlayerSymbol.X

    def test_get_player_by_symbol_not_found(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X)
        ]
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
        player = state.get_player_by_symbol("O")
        assert player is None

    def test_is_game_over(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X)
        ]
        
        # Game in progress
        state = GameState(
            board=[None] * 9,
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        assert state.is_game_over is False
        
        # Game finished
        state.status = GameStatus.FINISHED
        assert state.is_game_over is True
        
        # Game cancelled
        state.status = GameStatus.CANCELLED
        assert state.is_game_over is True

    def test_to_dict_and_from_dict(self):
        players = [
            PlayerScore(player_id="player1", symbol=PlayerSymbol.X, score=10),
            PlayerScore(player_id="player2", symbol=PlayerSymbol.O, score=5)
        ]
        original_state = GameState(
            board=[None, "X", None, "O", None, None, None, None, None],
            current_player_index=0,
            players=players,
            status=GameStatus.IN_PROGRESS,
            winner="player1",
            winning_sequence=[0, 1, 2],
            is_draw=False,
            move_count=2
        )
        
        # Convert to dict and back
        state_dict = original_state.to_dict()
        restored_state = GameState.from_dict(state_dict)
        
        # Verify all properties are preserved
        assert restored_state.board == original_state.board
        assert restored_state.current_player_index == original_state.current_player_index
        assert restored_state.status == original_state.status
        assert restored_state.winner == original_state.winner
        assert restored_state.winning_sequence == original_state.winning_sequence
        assert restored_state.is_draw == original_state.is_draw
        assert restored_state.move_count == original_state.move_count
        
        # Verify players are preserved
        assert len(restored_state.players) == len(original_state.players)
        for i, player in enumerate(restored_state.players):
            assert player.player_id == original_state.players[i].player_id
            assert player.symbol == original_state.players[i].symbol
            assert player.score == original_state.players[i].score 
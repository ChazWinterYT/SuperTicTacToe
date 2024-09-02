import pytest
from app.game_logic import Game, GameManager

def test_initial_game_state():
    game = Game()
    state = game.get_game_state()
    assert state["board"] == [None] * 9
    assert state["current_turn"] == "X"
    assert state["winner"] is None
    assert state["is_draw"] is False

def test_make_move():
    game = Game()
    assert game.make_move(0, "X") is True
    assert game.board[0] == "X"
    assert game.current_turn == "O"

    # Now try to make the same move as "O"
    assert game.make_move(0, "O") is False
    assert game.board[0] == "X"      # X should still be on the board
    assert game.current_turn == "O"  # Should still be O's turn

def test_check_winner():
    game = Game()
    game.make_move(0, "X")
    game.make_move(1, "X")
    game.make_move(2, "X")
    assert game.winner == "X"

def test_check_draw():
    game = Game()
    moves = [
        (0, "O"), (1, "X"), (2, "O"),
        (3, "X"), (4, "X"), (5, "O"),
        (6, "X"), (7, "O"), (8, "X")
    ]
    for index, player in moves:
        game.make_move(index, player)
    assert game.is_draw is True
    assert game.winner is None

def test_game_manager_create_and_get_game():
    manager = GameManager()
    game_id = "test_game"
    game = manager.create_game(game_id)
    assert manager.get_game(game_id) is game

def test_game_manager_handle_move():
    manager = GameManager()
    game_id = "test_game"
    state = manager.handle_move(game_id, 0, "X")
    assert state["board"][0] == "X"
    assert state["current_turn"] == "O"
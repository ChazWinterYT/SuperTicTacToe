from app.domain.entities.player import Player
from app.domain.entities.game import Game
from app.domain.value_objects.board_size import BoardSize

# Player factory functions
def create_player_1():
    return Player(player_id="player1", player_name="Player 1")

def create_player_2():
    return Player(player_id="player2", player_name="Player 2")

def create_player_3():
    return Player(player_id="player3", player_name="Player 3")

# Game factory functions
def create_standard_board_size():
    return BoardSize.create_standard()

def create_game_1():
    return Game(
        game_id="test-game",
        board_size=create_standard_board_size(),
        max_players=2
    )

def create_game_2():
    return Game(
        game_id="test-game-123",
        board_size=create_standard_board_size(),
        max_players=2
    )

CREATOR_ID = "creator-123"

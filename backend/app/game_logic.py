from typing import Optional, Dict

class Game:
    def __init__(self):
        self.board = [None] * 9  # 3x3 Tic-Tac-Toe board
        self.current_turn = "X"
        self.winner = None
        self.is_draw = False

    def make_move(self, index: int, player: str) -> bool:
        if self.board[index] is None and self.winner is None:
            self.board[index] = player
            self.check_winner()
            self.check_draw()
            self.current_turn = "O" if player == "X" else "X"
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],    # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],    # Columns
            [0, 4, 8], [2, 4, 6]                # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] and all(self.board[i] == self.board[combo[0]] for i in combo):
                self.winner = self.board[combo[0]]
                break

    def check_draw(self):
        if all(self.board):
            self.is_draw = True

    def get_game_state(self) -> dict:
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "winner": self.winner,
            "is_draw": self.is_draw
        }

class GameManager:
    def __init__(self):
        self.games: Dict[str, Game] = {}

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.games.get(game_id)

    def create_game(self, game_id: str) -> Game:
        game = Game()
        self.games[game_id] = game
        return game

    def handle_move(self, game_id: str, index: int, player: str) -> dict:
        game = self.get_game(game_id)
        if not game:
            game = self.create_game(game_id)

        game.make_move(index, player)
        return game.get_game_state()

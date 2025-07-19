from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
from app.core.exceptions import ValidationError


class GameStatus(Enum):
    """Enumeration of possible game statuses."""
    WAITING_FOR_PLAYERS = "waiting_for_players"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"


class PlayerSymbol(Enum):
    """Enumeration of player symbols."""
    X = "X"
    O = "O"
    TRIANGLE = "△"
    SQUARE = "□"
    DIAMOND = "◇"


@dataclass(frozen=True)
class PlayerScore:
    """Value object representing a player's score."""
    
    player_id: str
    symbol: PlayerSymbol
    score: int = 0
    sequences_completed: int = 0
    
    def add_points(self, points: int, sequences: int = 1) -> "PlayerScore":
        """Add points and sequences to the player's score."""
        return PlayerScore(
            player_id=self.player_id,
            symbol=self.symbol,
            score=self.score + points,
            sequences_completed=self.sequences_completed + sequences
        )


@dataclass
class GameState:
    """Value object representing the current state of a game."""
    
    board: List[Optional[str]]
    current_player_index: int
    players: List[PlayerScore]
    status: GameStatus
    winner: Optional[str] = None
    winning_sequence: Optional[List[int]] = None
    is_draw: bool = False
    move_count: int = 0
    
    def __post_init__(self):
        if not self.players:
            raise ValidationError("Game must have at least one player")
        
        if self.current_player_index >= len(self.players):
            raise ValidationError("Current player index out of bounds")
    
    @property
    def current_player(self) -> PlayerScore:
        """Get the current player."""
        return self.players[self.current_player_index]
    
    @property
    def next_player_index(self) -> int:
        """Get the index of the next player."""
        return (self.current_player_index + 1) % len(self.players)
    
    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.status in [GameStatus.FINISHED, GameStatus.CANCELLED]
    
    def get_player_by_id(self, player_id: str) -> Optional[PlayerScore]:
        """Get a player by their ID."""
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def get_player_by_symbol(self, symbol: str) -> Optional[PlayerScore]:
        """Get a player by their symbol."""
        for player in self.players:
            if player.symbol.value == symbol:
                return player
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the game state to a dictionary for serialization."""
        return {
            "board": self.board,
            "current_player_index": self.current_player_index,
            "players": [
                {
                    "player_id": p.player_id,
                    "symbol": p.symbol.value,
                    "score": p.score,
                    "sequences_completed": p.sequences_completed
                }
                for p in self.players
            ],
            "status": self.status.value,
            "winner": self.winner,
            "winning_sequence": self.winning_sequence,
            "is_draw": self.is_draw,
            "move_count": self.move_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameState":
        """Create a game state from a dictionary."""
        return cls(
            board=data["board"],
            current_player_index=data["current_player_index"],
            players=[
                PlayerScore(
                    player_id=p["player_id"],
                    symbol=PlayerSymbol(p["symbol"]),
                    score=p["score"],
                    sequences_completed=p["sequences_completed"]
                )
                for p in data["players"]
            ],
            status=GameStatus(data["status"]),
            winner=data.get("winner"),
            winning_sequence=data.get("winning_sequence"),
            is_draw=data.get("is_draw", False),
            move_count=data.get("move_count", 0)
        ) 
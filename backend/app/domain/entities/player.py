from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from app.core.exceptions import ValidationError


@dataclass
class Player:
    """Player entity representing a user in the game system."""
    
    id: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_seen: datetime = field(default_factory=datetime.utcnow)
    is_online: bool = False
    current_game_id: Optional[str] = None
    games_played: int = 0
    games_won: int = 0
    total_score: int = 0
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValidationError("Player name cannot be empty")
        
        if len(self.name.strip()) > 50:
            raise ValidationError("Player name cannot exceed 50 characters")
    
    @property
    def win_rate(self) -> float:
        """Calculate the player's win rate."""
        if self.games_played == 0:
            return 0.0
        return self.games_won / self.games_played
    
    @property
    def average_score(self) -> float:
        """Calculate the player's average score per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_score / self.games_played
    
    def join_game(self, game_id: str) -> None:
        """Join a game."""
        if self.current_game_id:
            raise ValidationError(f"Player {self.id} is already in game {self.current_game_id}")
        
        self.current_game_id = game_id
        self.is_online = True
        self.last_seen = datetime.utcnow()
    
    def leave_game(self) -> None:
        """Leave the current game."""
        self.current_game_id = None
    
    def go_offline(self) -> None:
        """Mark player as offline."""
        self.is_online = False
        self.last_seen = datetime.utcnow()
    
    def go_online(self) -> None:
        """Mark player as online."""
        self.is_online = True
        self.last_seen = datetime.utcnow()
    
    def update_last_seen(self) -> None:
        """Update the last seen timestamp."""
        self.last_seen = datetime.utcnow()
    
    def record_game_result(self, won: bool, score: int) -> None:
        """Record the result of a completed game."""
        self.games_played += 1
        if won:
            self.games_won += 1
        self.total_score += score
    
    def to_dict(self) -> dict:
        """Convert player to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "is_online": self.is_online,
            "current_game_id": self.current_game_id,
            "games_played": self.games_played,
            "games_won": self.games_won,
            "total_score": self.total_score,
            "win_rate": self.win_rate,
            "average_score": self.average_score
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """Create a player from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_seen=datetime.fromisoformat(data["last_seen"]),
            is_online=data["is_online"],
            current_game_id=data.get("current_game_id"),
            games_played=data.get("games_played", 0),
            games_won=data.get("games_won", 0),
            total_score=data.get("total_score", 0)
        ) 
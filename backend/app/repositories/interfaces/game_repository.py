from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.game import Game
from app.domain.value_objects.board_size import BoardSize


class GameRepository(ABC):
    """Abstract interface for game data access."""
    
    @abstractmethod
    async def create(self, game: Game) -> Game:
        """Create a new game."""
        pass
    
    @abstractmethod
    async def get_by_id(self, game_id: str) -> Optional[Game]:
        """Get a game by ID."""
        pass
    
    @abstractmethod
    async def get_active_games(self) -> List[Game]:
        """Get all active games."""
        pass
    
    @abstractmethod
    async def get_games_by_player(self, player_id: str) -> List[Game]:
        """Get all games for a specific player."""
        pass
    
    @abstractmethod
    async def get_public_games(self) -> List[Game]:
        """Get all public games that are waiting for players."""
        pass
    
    @abstractmethod
    async def get_games_by_board_size(self, board_size: BoardSize) -> List[Game]:
        """Get games by board size."""
        pass
    
    @abstractmethod
    async def update(self, game: Game) -> Game:
        """Update a game."""
        pass
    
    @abstractmethod
    async def delete(self, game_id: str) -> bool:
        """Delete a game."""
        pass
    
    @abstractmethod
    async def add_player_to_game(self, game_id: str, player_id: str) -> bool:
        """Add a player to a game."""
        pass
    
    @abstractmethod
    async def remove_player_from_game(self, game_id: str, player_id: str) -> bool:
        """Remove a player from a game."""
        pass
    
    @abstractmethod
    async def start_game(self, game_id: str) -> bool:
        """Start a game."""
        pass
    
    @abstractmethod
    async def end_game(self, game_id: str) -> bool:
        """End a game."""
        pass

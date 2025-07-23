from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.player import Player


class PlayerRepository(ABC):
    """Abstract interface for player data access."""
    
    @abstractmethod
    async def create(self, player: Player) -> Player:
        """Create a new player."""
        pass
    
    @abstractmethod
    async def get_by_id(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Player]:
        """Get a player by name."""
        pass
    
    @abstractmethod
    async def get_all_online(self) -> List[Player]:
        """Get all online players."""
        pass
    
    @abstractmethod
    async def get_all_in_lobby(self) -> List[Player]:
        """Get all players currently in the lobby (not in a game)."""
        pass
    
    @abstractmethod
    async def update(self, player: Player) -> Player:
        """Update a player."""
        pass
    
    @abstractmethod
    async def delete(self, player_id: str) -> bool:
        """Delete a player."""
        pass
    
    @abstractmethod
    async def mark_offline(self, player_id: str) -> bool:
        """Mark a player as offline."""
        pass
    
    @abstractmethod
    async def update_last_seen(self, player_id: str) -> bool:
        """Update a player's last seen timestamp."""
        pass

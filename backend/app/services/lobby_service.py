from typing import List, Optional
import uuid
from app.core.exceptions import LobbyError, ValidationError
from app.domain.entities.player import Player
from app.repositories.interfaces.player_repository import PlayerRepository


class LobbyService:
    """Service for managing the game lobby."""
    
    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository
    
    async def join_lobby(self, player_name: str) -> Player:
        """Join the lobby with a new player."""
        if not player_name or not player_name.strip():
            raise ValidationError("Player name cannot be empty")
        
        # Check if player name is already taken
        existing_player = await self.player_repository.get_by_name(player_name.strip())
        if existing_player:
            raise LobbyError(f"Player name '{player_name}' is already taken")
        
        # Create new player
        player = Player(
            player_id=str(uuid.uuid4()),
            player_name=player_name.strip()
        )
        
        # Save to repository
        await self.player_repository.create(player)
        
        return player
    
    async def leave_lobby(self, player_id: str) -> bool:
        """Leave the lobby."""
        player = await self.player_repository.get_by_id(player_id)
        if not player:
            raise LobbyError("Player not found")
        
        # Mark player as offline
        await self.player_repository.mark_offline(player_id)
        
        return True
    
    async def get_lobby_players(self) -> List[Player]:
        """Get all players currently in the lobby."""
        return await self.player_repository.get_all_in_lobby()
    
    async def get_online_players(self) -> List[Player]:
        """Get all online players."""
        return await self.player_repository.get_all_online()
    
    async def get_player(self, player_id: str) -> Optional[Player]:
        """Get a specific player."""
        return await self.player_repository.get_by_id(player_id)
    
    async def update_player_status(self, player_id: str) -> bool:
        """Update a player's last seen timestamp."""
        return await self.player_repository.update_last_seen(player_id)
    
    async def challenge_player(self, challenger_id: str, challenged_player_id: str) -> dict:
        """Challenge another player to a game."""
        challenger = await self.player_repository.get_by_id(challenger_id)
        if not challenger:
            raise LobbyError("Challenger not found")
        
        challenged = await self.player_repository.get_by_id(challenged_player_id)
        if not challenged:
            raise LobbyError("Challenged player not found")
        
        if challenger_id == challenged_player_id:
            raise LobbyError("Cannot challenge yourself!")
        
        if not challenged.is_online:
            raise LobbyError("Challenged player is not online")
        
        if challenged.current_game_id:
            raise LobbyError("Challenged player is already in a game")
        
        return {
            "challenger": challenger.to_dict(),
            "challenged": challenged.to_dict(),
            "message": f"{challenger.player_name} challenged {challenged.player_name} to a game!"
        }
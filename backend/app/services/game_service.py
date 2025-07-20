from typing import List, Optional, Dict, Any
import uuid
from app.core.exceptions import GameError, ValidationError
from app.core.config import settings
from app.domain.entities.game import Game
from app.domain.entities.player import Player
from app.domain.value_objects.board_size import BoardSize
from app.repositories.interfaces.game_repository import GameRepository
from app.repositories.interfaces.player_repository import PlayerRepository


class GameService:
    """Service for managing games."""
    
    def __init__(self, game_repository: GameRepository, player_repository: PlayerRepository):
        self.game_repository = game_repository
        self.player_repository = player_repository
    
    async def create_game(
        self,
        board_size: BoardSize,
        max_players: int,
        is_public: bool = True,
        creator_id: str = 'default_creator_id'  # Provide a default for testing
    ) -> Game:
        """Create a new game."""
        # Validate creator exists
        creator = await self.player_repository.get_by_id(creator_id)
        if not creator:
            raise GameError("Creator not found")
        
        # Validate max players
        if max_players < settings.min_players or max_players > settings.max_players:
            raise GameError(f"Max players must be between {settings.min_players} and {settings.max_players}")
        
        # Create game
        game = Game(
            id=str(uuid.uuid4()),
            board_size=board_size,
            max_players=max_players,
            creator_id=creator_id,
            is_public=is_public
        )
        
        # Add creator to game
        game.add_player(creator)
        
        # Save game
        await self.game_repository.create(game)
        
        return game
    
    async def join_game(self, game_id: str, player_id: str) -> Game:
        """Join an existing game."""
        game = await self.game_repository.get_by_id(game_id)
        if not game:
            raise GameError("Game not found")
        
        if game.is_full:
            raise GameError("Game is full")
        
        if game.started_at:
            raise GameError("Cannot join a game that has already started")
        
        player = await self.player_repository.get_by_id(player_id)
        if not player:
            raise GameError("Player not found")
        
        if player.current_game_id:
            raise GameError("Player is already in a game")
        
        # Add player to game
        game.add_player(player)
        
        # Update game
        await self.game_repository.update(game)
        
        return game
    
    async def leave_game(self, game_id: str, player_id: str) -> Game:
        """Leave a game."""
        game = await self.game_repository.get_by_id(game_id)
        if not game:
            raise GameError("Game not found")
        
        if game.is_active:
            raise GameError("Cannot leave an active game")
        
        # Remove player from game
        game.remove_player(player_id)
        
        # Update game
        await self.game_repository.update(game)
        
        return game
    
    async def start_game(self, game_id: str, player_id: str) -> Game:
        """Start a game."""
        game = await self.game_repository.get_by_id(game_id)
        if not game:
            raise GameError("Game not found")
        
        if game.creator_id != player_id:
            raise GameError("Only the creator can start the game")
        
        if not game.can_start:
            raise GameError("Game cannot start")
        
        # Start the game
        game.start_game()
        
        # Update game
        await self.game_repository.update(game)
        
        return game
    
    async def make_move(self, game_id: str, player_id: str, position: int) -> Dict[str, Any]:
        """Make a move in a game."""
        game = await self.game_repository.get_by_id(game_id)
        if not game:
            raise GameError("Game not found")
        
        if not game.is_active:
            raise GameError("Game is not active")
        
        # Make the move
        game_state = game.make_move(player_id, position)
        
        # Update game
        await self.game_repository.update(game)
        
        return game_state
    
    async def get_game(self, game_id: str) -> Optional[Game]:
        """Get a game by ID."""
        return await self.game_repository.get_by_id(game_id)
    
    async def get_public_games(self) -> List[Game]:
        """Get all public games waiting for players."""
        return await self.game_repository.get_public_games()
    
    async def get_player_games(self, player_id: str) -> List[Game]:
        """Get all games for a player."""
        return await self.game_repository.get_games_by_player(player_id)
    
    async def get_active_games(self) -> List[Game]:
        """Get all active games."""
        return await self.game_repository.get_active_games()
    
    async def delete_game(self, game_id: str, player_id: str) -> bool:
        """Delete a game (only creator can delete)."""
        game = await self.game_repository.get_by_id(game_id)
        if not game:
            raise GameError("Game not found")
        
        if game.creator_id != player_id:
            raise GameError("Only the creator can delete the game")
        
        if game.is_active:
            raise GameError("Cannot delete an active game")
        
        return await self.game_repository.delete(game_id)

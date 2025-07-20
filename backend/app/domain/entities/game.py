from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
from app.core.exceptions import GameError, ValidationError
from app.domain.value_objects.board_size import BoardSize
from app.domain.value_objects.game_state import GameState, GameStatus, PlayerSymbol, PlayerScore
from app.domain.entities.player import Player


@dataclass
class Game:
    """Game entity representing a tic-tac-toe game."""
    
    game_id: str
    board_size: BoardSize
    max_players: int
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    players: List[Player] = field(default_factory=list)
    game_state: Optional[GameState] = None
    is_public: bool = True
    creator_id: Optional[str] = None
    
    def __post_init__(self):
        if not self.game_id:
            self.game_id = str(uuid.uuid4())
        self.validate()
        
    def validate(self) -> None:
        if self.max_players < 2:
            raise ValidationError("Game must have at least 2 players")
        
        if self.max_players > 4:
            raise ValidationError("Game cannot have more than 4 players")
    
    @property
    def status(self) -> GameStatus:
        """Get the current game status."""
        if not self.game_state:
            return GameStatus.WAITING_FOR_PLAYERS
        
        return self.game_state.status
    
    @property
    def is_full(self) -> bool:
        """Check if the game is full."""
        return len(self.players) >= self.max_players
    
    @property
    def can_start(self) -> bool:
        """Check if the game can start."""
        return len(self.players) >= 2 and not self.started_at
    
    @property
    def is_active(self) -> bool:
        """Check if the game is currently active."""
        return bool(self.started_at and not self.finished_at)
    
    def add_player(self, player: Player) -> None:
        """Add a player to the game."""
        if self.is_full:
            raise GameError("Game is full")
        
        if self.started_at:
            raise GameError("Cannot add players to a game that has already started")
        
        if any(p.player_id == player.player_id for p in self.players):
            raise GameError("Player is already in the game")
        
        self.players.append(player)
        player.join_game(self.game_id)

    def remove_player(self, player_id: str) -> None:
        """Remove a player from the game."""
        player = self.get_player(player_id)
        if not player:
            raise GameError("Player not found in game")
        
        if self.is_active:
            raise GameError("Cannot remove players from an active game")
        
        self.players = [p for p in self.players if p.player_id != player_id]
        player.leave_game()
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def start_game(self) -> None:
        """Start the game."""
        if not self.can_start:
            raise GameError("Game cannot start")
        
        if len(self.players) < 2:
            raise GameError("Need at least 2 players to start")
        
        self.started_at = datetime.utcnow()
        
        # Initialize game state
        available_symbols = list(PlayerSymbol)[:self.max_players]
        player_scores = [
            PlayerScore(
                player_id=player.player_id,
                symbol=available_symbols[i]
            )
            for i, player in enumerate(self.players)
        ]
        
        self.game_state = GameState(
            board=[None] * self.board_size.total_cells,
            current_player_index=0,
            players=player_scores,
            status=GameStatus.IN_PROGRESS
        )
    
    def make_move(self, player_id: str, position: int) -> Dict[str, Any]:
        """Make a move in the game."""
        if not self.is_active:
            raise GameError("Game is not active")
        
        if not self.game_state:
            raise GameError("Game state not initialized")
        
        # Validate player's turn
        current_player = self.game_state.current_player
        if current_player.player_id != player_id:
            raise GameError("Not your turn")
        
        # Validate position
        if position < 0 or position >= self.board_size.total_cells:
            raise GameError("Invalid position")
        
        if self.game_state.board[position] is not None:
            raise GameError("Position already occupied")
        
        # Make the move
        symbol = current_player.symbol.value
        self.game_state.board[position] = symbol
        self.game_state.move_count += 1
        
        # Check for winning sequences
        winning_sequences = self._check_winning_sequences(symbol, position)
        
        if winning_sequences:
            # Award points for each winning sequence
            points = self._calculate_points(winning_sequences)
            self._update_player_score(player_id, points, len(winning_sequences))
            
            # Check if game should end
            if self._should_end_game():
                self._end_game()
            else:
                # Continue to next player
                self.game_state.current_player_index = self.game_state.next_player_index
        else:
            # No winning sequences, continue to next player
            self.game_state.current_player_index = self.game_state.next_player_index
        
        return self.game_state.to_dict()
    
    def _check_winning_sequences(self, symbol: str, position: int) -> List[List[int]]:
        """Check for winning sequences after a move."""
        if not self.game_state:
            return []
            
        winning_sequences = []
        all_sequences = self.board_size.get_winning_sequences()
        
        for sequence in all_sequences:
            if position in sequence:
                # Check if this sequence is now complete for the symbol
                if all(self.game_state.board[i] == symbol for i in sequence):
                    winning_sequences.append(sequence)
        
        return winning_sequences
    
    def _calculate_points(self, sequences: List[List[int]]) -> int:
        """Calculate points for winning sequences."""
        from app.core.config import settings
        
        total_points = 0
        for sequence in sequences:
            # Base points for 3-in-a-row
            base_points = settings.base_score
            
            # Bonus points for longer sequences
            if len(sequence) > 3:
                bonus_multiplier = settings.sequence_multiplier ** (len(sequence) - 3)
                base_points = int(base_points * bonus_multiplier)
            
            total_points += base_points
        
        return total_points
    
    def _update_player_score(self, player_id: str, points: int, sequences: int) -> None:
        """Update a player's score."""
        if not self.game_state:
            return
            
        for i, player_score in enumerate(self.game_state.players):
            if player_score.player_id == player_id:
                self.game_state.players[i] = player_score.add_points(points, sequences)
                break
    
    def _should_end_game(self) -> bool:
        """Determine if the game should end."""
        if not self.game_state:
            return False
            
        # Game ends when board is full or a player has a significant lead
        if self.game_state.move_count >= self.board_size.total_cells:
            return True
        
        # Check if any player has a significant lead (e.g., 3x the base score)
        from app.core.config import settings
        max_score = max(p.score for p in self.game_state.players)
        min_score = min(p.score for p in self.game_state.players)
        
        return max_score >= min_score + (settings.base_score * 3)
    
    def _end_game(self) -> None:
        """End the game and determine winner."""
        if not self.game_state:
            return
            
        self.finished_at = datetime.utcnow()
        self.game_state.status = GameStatus.FINISHED
        
        # Determine winner (player with highest score)
        winner = max(self.game_state.players, key=lambda p: p.score)
        self.game_state.winner = winner.player_id
        
        # Update player statistics
        for player in self.players:
            player_score = self.game_state.get_player_by_id(player.player_id)
            if player_score:
                won = player.player_id == winner.player_id
                player.record_game_result(won, player_score.score)
    
    @property
    def player_ids(self) -> List[str]:
        """Return list of player IDs."""
        return [player.player_id for player in self.players]

    def to_dict(self) -> Dict[str, Any]:
        """Convert game to dictionary for serialization."""
        return {
            "game_id": self.game_id,
            "board_size": str(self.board_size),
            "max_players": self.max_players,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "players": [p.to_dict() for p in self.players],
            "player_ids": self.player_ids,
            "game_state": self.game_state.to_dict() if self.game_state else None,
            "status": self.status.value,
            "is_public": self.is_public,
            "creator_id": self.creator_id
        }

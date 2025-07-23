from typing import List, Tuple
from dataclasses import dataclass
from app.core.exceptions import ValidationError
from app.core.config import settings


@dataclass(frozen=True)
class BoardSize:
    """Value object representing a board size with validation."""
    
    width: int
    height: int
    
    def __post_init__(self):
        if not settings.min_board_size <= self.width <= settings.max_board_size:
            raise ValidationError(
                f"Board width must be between {settings.min_board_size} and {settings.max_board_size}"
            )
        
        if not settings.min_board_size <= self.height <= settings.max_board_size:
            raise ValidationError(
                f"Board height must be between {settings.min_board_size} and {settings.max_board_size}"
            )
    
    @property
    def total_cells(self) -> int:
        """Get the total number of cells in the board."""
        return self.width * self.height
    
    @property
    def is_square(self) -> bool:
        """Check if the board is square."""
        return self.width == self.height
    
    def get_winning_sequences(self) -> List[List[int]]:
        """Get all possible winning sequences for this board size."""
        sequences = []
        
        # Rows
        for row in range(self.height):
            row_start = row * self.width
            for col in range(self.width - 2):  # Need at least 3 in a row
                sequence = [row_start + col + i for i in range(3)]
                if sequence[-1] < self.total_cells:
                    sequences.append(sequence)
        
        # Columns
        for col in range(self.width):
            for row in range(self.height - 2):  # Need at least 3 in a column
                sequence = [(row + i) * self.width + col for i in range(3)]
                if sequence[-1] < self.total_cells:
                    sequences.append(sequence)
        
        # Diagonals (main diagonal)
        for start_row in range(self.height - 2):
            for start_col in range(self.width - 2):
                # Main diagonal
                sequence = [(start_row + i) * self.width + (start_col + i) for i in range(3)]
                if sequence[-1] < self.total_cells:
                    sequences.append(sequence)
                
                # Anti-diagonal
                sequence = [(start_row + i) * self.width + (start_col + 2 - i) for i in range(3)]
                if sequence[-1] < self.total_cells:
                    sequences.append(sequence)
        
        return sequences
    
    @classmethod
    def create_square(cls, size: int) -> "BoardSize":
        """Create a square board of the given size."""
        return cls(size, size)
    
    @classmethod
    def create_standard(cls) -> "BoardSize":
        """Create a standard 3x3 tic-tac-toe board."""
        return cls.create_square(3)
    
    def __str__(self) -> str:
        return f"{self.width}x{self.height}"
    
    def __repr__(self) -> str:
        return f"BoardSize({self.width}, {self.height})"

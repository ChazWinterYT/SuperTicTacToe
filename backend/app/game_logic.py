from typing import List, Optional

def check_winner(board: List[Optional[str]]) -> Optional[str]:
    """Check if there is a winner on the board"""
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],    # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8],    # Vertical
        [0, 4, 8], [2, 4, 6],               # Diagonal
    ]

    for combo in winning_combinations:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    
    return None

def is_board_full(board: List[Optional[str]]) -> bool:
    """Check if the board is full"""
    return all(cell is not None for cell in board)

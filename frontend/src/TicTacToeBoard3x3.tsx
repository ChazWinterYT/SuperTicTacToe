import React, { useState, useEffect } from 'react';
import './TicTacToeBoard.css';

const TicTacToeBoard3x3: React.FC = () => {
    const [board, setBoard] = useState(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState(true);
    const [winningLine, setWinningLine] = useState<number[] | null>(null);
    const [winner, setWinner] = useState<string | null>(null);

    const handleClick = (index: number) => {
        if (board[index] || winner) {
            return;
        }

        const newBoard = board.slice();
        newBoard[index] = isXNext ? 'X' : 'O';
        setBoard(newBoard);
        setIsXNext(!isXNext);
    };

    const renderSquare = (index: number) => (
        <button
            className={`square ${winningLine && winningLine.includes(index) ? 'winning-square' : ''}`}
            onClick={() => handleClick(index)}
        >
            {board[index]}
        </button>
    );

    const checkIfWinner = (board: string[]) => {
        const lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],    // Horizontal
            [0, 3, 6], [1, 4, 7], [2, 5, 8],    // Vertical
            [0, 4, 8], [2, 4, 6],               // Diagonal
        ];
        for (let i = 0; i < lines.length; i++) {
            const [a, b, c] = lines[i];
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return { winner: board[a], line: lines[i] };
            }
        }
        return null;
    };

    useEffect(() => {
        const result = checkIfWinner(board);
        if (result) {
            setWinner(result.winner);
            setWinningLine(result.line);
        }
    }, [board]);

    const isBoardFull = (board: string[]) => {
        return board.every(square => square !== null);
    };

    const resetGame = () => {
        setBoard(Array(9).fill(null));
        setIsXNext(true);
        setWinningLine(null);
        setWinner(null);
    };

    const currentStatus = winner
        ? `${winner} Wins!`
        : isBoardFull(board)
            ? "It's a Draw!"
            : `${isXNext ? 'X' : 'O'}'s turn`;

    return (
        <div className="game-container">
            <div className="status">{currentStatus}</div>
            <div className="board">
                {Array.from({ length: 9 }).map((_, index) => renderSquare(index))}
            </div>
            <div className='play-again-leave-space'>
                {(winner || isBoardFull(board)) && (
                    <button className="play-again" onClick={resetGame}>
                        Play Again
                    </button>
                )}
            </div>
        </div>
    );
};

export default TicTacToeBoard3x3;

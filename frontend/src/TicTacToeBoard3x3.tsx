import React, { useState } from 'react';
import './TicTacToeBoard.css';

const TicTacToeBoard3x3: React.FC = () => {
    const [board, setBoard] = useState(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState(true);

    const handleClick = (index: number) => {
        const newBoard = board.slice();
        if (newBoard[index] || winner) {
            // Block moves if the square is already occupied or there is a winner already
            return;
        }
        newBoard[index] = isXNext ? 'X' : 'O';
        setBoard(newBoard);
        setIsXNext(!isXNext);
    };

    const renderSquare = (index: number) => (
        <button className="square" onClick={() => handleClick(index)}>
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
                return board[a];
            }
        }
        return null;
    };

    const winner = checkIfWinner(board);
    const isBoardFull = (board: string[]) => {
        return board.every(square => square !== null);
    };
    
    let currentStatus;
    if (winner) {
        currentStatus = `${winner} Wins!`;
    } else if (isBoardFull(board)) {
        currentStatus = "It's a Draw :/";
    } else {
        currentStatus = `${isXNext ? 'X' : 'O'}'s turn`
    }

    return (
        <div>
            <div className='status'>{currentStatus}</div>
            <div className="board">
                <div className="board-row">
                    {renderSquare(0)}
                    {renderSquare(1)}
                    {renderSquare(2)}
                </div>
                <div className="board-row">
                    {renderSquare(3)}
                    {renderSquare(4)}
                    {renderSquare(5)}
                </div>
                <div className="board-row">
                    {renderSquare(6)}
                    {renderSquare(7)}
                    {renderSquare(8)}
                </div>
            </div>
        </div>
    );
};

export default TicTacToeBoard3x3;
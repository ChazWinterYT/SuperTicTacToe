import React, { useState } from 'react';
import './TicTacToeBoard.css';

const TicTacToeBoard3x3: React.FC = () => {
    const [board, setBoard] = useState(Array(9).fill(null));
    const [isXNext, setIsXNext] = useState(true);

    const handleClick = (index: number) => {
        const newBoard = board.slice();
        if (newBoard[index]) {
            // Don't allow user to place X or O if the cell is already filled
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

    return (
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
    );
};

export default TicTacToeBoard3x3;
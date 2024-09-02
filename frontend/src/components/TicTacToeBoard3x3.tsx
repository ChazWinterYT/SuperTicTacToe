import React from 'react';
import useWebSocket from '../services/WebSocketService';
import './TicTacToeBoard.css';

interface TicTacToeBoard3x3Props {
    gameId: string;
    player: string; // 'X' or 'O'
}

const TicTacToeBoard3x3: React.FC<TicTacToeBoard3x3Props> = ({ gameId, player }) => {
    const { gameState, sendMove } = useWebSocket(gameId, player);

    const handleClick = (index: number) => {
        if (gameState.board[index] || gameState.winner || gameState.isDraw) {
            return;
        }
        sendMove(index);
    };

    const renderSquare = (index: number) => (
        <button key={index} className="square" onClick={() => handleClick(index)}>
            {gameState.board[index]}
        </button>
    );

    let status;
    if (gameState.winner) {
        status = `${gameState.winner} Wins!`;
    } else if (gameState.isDraw) {
        status = "It's a Draw :/";
    } else {
        status = `${gameState.isXNext ? 'X' : 'O'}'s turn`;
    }

    const resetGame = () => {
        // TODO: Implement reset logic, possibly through a new WebSocket message
    };

    return (
        <div className="game-container">
            <div className="status">{status}</div>
            <div className="board">
                {Array.from({ length: 9 }).map((_, index) => renderSquare(index))}
            </div>
            <div className="play-again-leave-space">
                {(gameState.winner || gameState.isDraw) && (
                    <button className="play-again" onClick={resetGame}>
                        Play Again
                    </button>
                )}
            </div>
        </div>
    );
};

export default TicTacToeBoard3x3;

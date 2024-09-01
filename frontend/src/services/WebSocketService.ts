import { useEffect, useRef, useState } from "react";

interface GameState {
    board: (string | null)[];
    isXNext: boolean;
    winner: string | null;
    isDraw: boolean;
}

const useWebSocket = (gameId: string, player: string) => {
    const [gameState, setGameState] = useState<GameState>({
        board: Array(9).fill(null),
        isXNext: true,
        winner: null,
        isDraw: false,
    });

    // Keep a reference to this WebSocket so we can reuse it
    const socketRef = useRef<WebSocket | null>(null);

    useEffect(() => {
        const socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${player}`);
        
        socket.onopen = () => {
            console.log("WebSocket connected!");
            socketRef.current = socket;
        };

        socket.onmessage = (event) => {
            const data: GameState = JSON.parse(event.data);
            setGameState(data);
        };

        socket.onclose = () => {
            console.log("WebSocket disconnected!");
            socketRef.current = null;
        };

        return () => {
            socket.close();
        };
    }, [gameId, player]);

    const sendMove = (index: number) => {
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ index }));
        }
    };

    return { gameState, sendMove };
};

export default useWebSocket;
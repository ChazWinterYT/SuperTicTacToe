# Project Structure

This project is organized into two main parts: the frontend and the backend. The frontend is responsible for the user interface and game interactions, while the backend handles the game logic, player management, and real-time communication.

## Frontend (React + TypeScript)

- **components/**: Contains all reusable React components, including the game board (`TicTacToeBoard3x3.tsx`), lobby (`Lobby.tsx`), and version display (`Version.tsx`).
- **services/**: Contains service files for handling WebSocket connections and API calls.
- **App.tsx**: The main component that orchestrates the application layout and integrates the game board and lobby.
- **public/**: Contains static assets like the HTML template and favicon.

## Backend (FastAPI + WebSocket)

- **app/**: Contains the core FastAPI application, including:
  - **main.py**: The entry point that initializes the FastAPI app and includes routers.
  - **lobby.py**: Handles player management, such as joining the lobby and challenging other players.
  - **game.py**: Manages game state and logic.
  - **websocket.py**: Manages WebSocket connections for real-time communication between players.
  - **models.py**: Defines data models like `Player` and `GameState`.
  - **utils.py**: Contains utility functions like game ID generation.
  
- **requirements.txt**: Lists the Python packages required for the backend.
- **template.yaml**: AWS SAM template for deploying the backend to AWS Lambda and API Gateway.
- **samconfig.toml**: Configuration file for SAM CLI to manage deployment settings.


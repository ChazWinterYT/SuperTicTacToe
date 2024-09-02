# SuperTicTacToe
Tic Tac Toe game, potentially with multiplayer support

# Files
TicTacToeProject/
│
├── frontend/                # Frontend codebase
│   ├── public/              # Public assets (favicon, index.html, etc.)
│   ├── src/                 # React source files
│   │   ├── components/      # Reusable components
│   │   │   ├── TicTacToeBoard3x3.tsx  # Main Tic Tac Toe game component
│   │   │   ├── Lobby.tsx               # Lobby component for player list and challenges
│   │   │   └── Version.tsx             # Version component to display app version
│   │   ├── services/        # Service files for WebSocket, API calls
│   │   │   ├── WebSocketService.ts     # WebSocket service for real-time communication
│   │   ├── App.tsx          # Main application component
│   │   ├── index.tsx        # Entry point for React
│   │   ├── App.css          # Global styles
│   │   └── index.css        # Root styles
│   ├── package.json         # NPM dependencies and scripts
│   ├── tsconfig.json        # TypeScript configuration
│   └── .env                 # Environment variables
│
├── backend/                 # Backend codebase
│   ├── app/                 # FastAPI application
│   │   ├── main.py          # Entry point for FastAPI
│   │   ├── lobby.py         # Lobby management (players, challenges)
│   │   ├── game_logic.py    # Game logic and state management
│   │   ├── websocket.py     # WebSocket handling for real-time communication
│   │   ├── models.py        # Data models (Player, GameState)
│   │   ├── utils.py         # Utility functions (e.g., ID generation)
│   │   └── __init__.py      # Python package initialization
│   ├── requirements.txt     # Python dependencies
│   ├── template.yaml        # SAM template for AWS deployment
│   └── samconfig.toml       # SAM configuration file
│
├── .gitignore               # Files and directories to be ignored by Git
├── README.md                # Project documentation (this file)
└── deploy.yml               # GitHub Actions workflow for deployment

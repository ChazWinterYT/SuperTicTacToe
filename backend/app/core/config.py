from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "Super Tic Tac Toe API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API
    api_v1_prefix: str = "/api/v1"
    api_gateway_url: str = "http://localhost:8000"
    
    # CORS
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "https://chazwinter.com",
        "https://www.chazwinter.com"
    ]
    
    # Database
    dynamodb_table_name: str = "SuperTicTacToe"
    aws_region: str = "us-east-1"
    
    # WebSocket
    websocket_ping_interval: int = 20
    websocket_ping_timeout: int = 20
    
    # Game Settings
    max_board_size: int = 15
    min_board_size: int = 3
    max_players: int = 4
    min_players: int = 2
    
    # Scoring
    base_score: int = 10
    sequence_multiplier: float = 1.5
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


# Global settings instance
settings = Settings()

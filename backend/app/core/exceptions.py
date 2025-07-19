from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


class SuperTicTacToeException(Exception):
    """Base exception for the application."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(SuperTicTacToeException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class NotFoundError(SuperTicTacToeException):
    """Raised when a resource is not found."""
    
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f"{resource} with id {resource_id} not found",
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "resource_id": resource_id}
        )


class DatabaseError(SuperTicTacToeException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class GameError(SuperTicTacToeException):
    """Raised when game logic errors occur."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="GAME_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class LobbyError(SuperTicTacToeException):
    """Raised when lobby-related errors occur."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="LOBBY_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class WebSocketError(SuperTicTacToeException):
    """Raised when WebSocket-related errors occur."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="WEBSOCKET_ERROR",
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


def handle_super_tictactoe_exception(exc: SuperTicTacToeException) -> HTTPException:
    """Convert custom exceptions to FastAPI HTTP exceptions."""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    ) 
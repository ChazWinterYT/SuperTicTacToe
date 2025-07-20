import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    SuperTicTacToeException,
    ValidationError,
    NotFoundError,
    GameError,
    LobbyError,
    WebSocketError,
    handle_super_tictactoe_exception
)


class TestSuperTicTacToeException:
    def test_base_exception_creation(self):
        exc = SuperTicTacToeException("Test message")
        assert exc.message == "Test message"
        assert exc.error_code == "INTERNAL_ERROR"
        assert exc.status_code == 500
        assert exc.details == {}

    def test_exception_with_custom_values(self):
        exc = SuperTicTacToeException(
            message="Custom error",
            error_code="CUSTOM_ERROR",
            status_code=400,
            details={"key": "value"}
        )
        assert exc.message == "Custom error"
        assert exc.error_code == "CUSTOM_ERROR"
        assert exc.status_code == 400
        assert exc.details == {"key": "value"}


class TestValidationError:
    def test_validation_error_creation(self):
        exc = ValidationError("Invalid input")
        assert exc.message == "Invalid input"
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.status_code == 400

    def test_validation_error_with_details(self):
        exc = ValidationError("Invalid input", {"field": "name", "value": ""})
        assert exc.message == "Invalid input"
        assert exc.details == {"field": "name", "value": ""}


class TestNotFoundError:
    def test_not_found_error_creation(self):
        exc = NotFoundError("Player", "player-123")
        assert exc.message == "Player with id player-123 not found"
        assert exc.error_code == "NOT_FOUND"
        assert exc.status_code == 404
        assert exc.details == {"resource": "Player", "resource_id": "player-123"}


class TestGameError:
    def test_game_error_creation(self):
        exc = GameError("Game is full")
        assert exc.message == "Game is full"
        assert exc.error_code == "GAME_ERROR"
        assert exc.status_code == 400


class TestLobbyError:
    def test_lobby_error_creation(self):
        exc = LobbyError("Player not found")
        assert exc.message == "Player not found"
        assert exc.error_code == "LOBBY_ERROR"
        assert exc.status_code == 400


class TestWebSocketError:
    def test_websocket_error_creation(self):
        exc = WebSocketError("Connection failed")
        assert exc.message == "Connection failed"
        assert exc.error_code == "WEBSOCKET_ERROR"
        assert exc.status_code == 400


class TestExceptionHandler:
    def test_handle_super_tictactoe_exception(self):
        exc = ValidationError("Test error")
        response = handle_super_tictactoe_exception(exc)
        
        assert isinstance(response, HTTPException)
        assert response.status_code == 400
        assert response.detail == {
            "error_code": "VALIDATION_ERROR",
            "message": "Test error",
            "details": {}
        } 
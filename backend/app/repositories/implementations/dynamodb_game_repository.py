import boto3
from typing import List, Optional
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
from app.core.config import settings
from app.core.exceptions import NotFoundError, DatabaseError
from app.domain.entities.game import Game
from app.domain.entities.player import Player
from app.domain.value_objects.board_size import BoardSize
from app.domain.value_objects.game_state import GameState
from app.repositories.interfaces.game_repository import GameRepository
from app.repositories.interfaces.player_repository import PlayerRepository


class DynamoDBGameRepository(GameRepository):
    """DynamoDB implementation of the game repository."""

    def __init__(self, player_repository: PlayerRepository):
        self.player_repository = player_repository
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.aws_region)
        self.table = self.dynamodb.Table(f"{settings.dynamodb_table_name}-Games")
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.aws_region)
        self.table = self.dynamodb.Table(f"{settings.dynamodb_table_name}-Games")

    async def create(self, game: Game) -> Game:
        # Ensure player_repository is available
        if not self.player_repository:
            raise DatabaseError("Player repository is not set.")
        """Create a new game."""
        try:
            self.table.put_item(Item=game.to_dict())
            return game
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to create game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error creating game: {str(e)}")

    async def get_by_id(self, game_id: str) -> Optional[Game]:
        """Get a game by ID."""
        try:
            response = self.table.get_item(Key={"game_id": game_id})
            if "Item" not in response:
                return None

            return self._dict_to_game(response["Item"])
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get game by ID: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting game by ID: {str(e)}")

    async def get_active_games(self) -> List[Game]:
        """Get all active games."""
        try:
            response = self.table.scan(
                FilterExpression="attribute_exists(started_at) AND attribute_not_exists(finished_at)"
            )

            return [self._dict_to_game(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get active games: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting active games: {str(e)}")

    async def get_games_by_player(self, player_id: str) -> List[Game]:
        """Get all games for a specific player."""
        try:
            response = self.table.query(
                IndexName="PlayerIdIndex",
                KeyConditionExpression="player_id = :player_id",
                ExpressionAttributeValues={":player_id": player_id}
            )

            return [self._dict_to_game(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get games by player: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting games by player: {str(e)}")

    async def get_public_games(self) -> List[Game]:
        """Get all public games that are waiting for players."""
        try:
            response = self.table.scan(
                FilterExpression="is_public = :is_public AND attribute_not_exists(started_at)",
                ExpressionAttributeValues={":is_public": True}
            )

            return [self._dict_to_game(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get public games: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting public games: {str(e)}")

    async def get_games_by_board_size(self, board_size: BoardSize) -> List[Game]:
        """Get games by board size."""
        try:
            response = self.table.scan(
                FilterExpression="board_size = :board_size",
                ExpressionAttributeValues={":board_size": str(board_size)}
            )

            return [self._dict_to_game(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get games by board size: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting games by board size: {str(e)}")

    async def update(self, game: Game) -> Game:
        """Update a game."""
        try:
            self.table.put_item(Item=game.to_dict())
            return game
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to update game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error updating game: {str(e)}")

    async def delete(self, game_id: str) -> bool:
        """Delete a game."""
        try:
            response = self.table.delete_item(Key={"game_id": game_id})
            return "Attributes" in response
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to delete game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error deleting game: {str(e)}")

    async def add_player_to_game(self, game_id: str, player_id: str) -> bool:
        """Add a player to a game."""
        try:
            game = await self.get_by_id(game_id)
            if not game:
                return False

            # This would need to be implemented with proper player lookup
            # For now, just update the game
            await self.update(game)
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to add player to game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error adding player to game: {str(e)}")

    async def remove_player_from_game(self, game_id: str, player_id: str) -> bool:
        """Remove a player from a game."""
        try:
            game = await self.get_by_id(game_id)
            if not game:
                return False

            # This would need to be implemented with proper player lookup
            # For now, just update the game
            await self.update(game)
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to remove player from game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error removing player from game: {str(e)}")

    async def start_game(self, game_id: str) -> bool:
        """Start a game."""
        try:
            game = await self.get_by_id(game_id)
            if not game:
                return False

            game.start_game()
            await self.update(game)
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to start game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error starting game: {str(e)}")

    async def end_game(self, game_id: str) -> bool:
        """End a game."""
        try:
            game = await self.get_by_id(game_id)
            if not game:
                return False

            game.finished_at = datetime.utcnow()
            await self.update(game)
            
            # Clear current_game_id for each player
            for player in game.players:
                player.current_game_id = None
                await self.player_repository.update(player)
            
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to end game: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error ending game: {str(e)}")

    def _dict_to_game(self, data: dict) -> Game:
        """Convert dictionary to Game entity."""      
        # Parse board size
        board_size_str = data.get("board_size", "3x3")
        width, height = map(int, board_size_str.split("x"))
        board_size = BoardSize(width, height)

        # Create game with basic data
        game = Game(
            game_id=data["game_id"],
            board_size=board_size,
            max_players=data.get("max_players", 2),
            created_at=datetime.fromisoformat(data["created_at"]),
            is_public=data.get("is_public", True),
            creator_id=data.get("creator_id")
        )

        # Parse timestamps
        if data.get("started_at"):
            game.started_at = datetime.fromisoformat(data["started_at"])
        if data.get("finished_at"):
            game.finished_at = datetime.fromisoformat(data["finished_at"])

        # Parse players (simplified)
        if "players" in data:
            game.players = [Player.from_dict(p) for p in data["players"]]

        # Parse game state (simplified)
        if "game_state" in data and data["game_state"]:
            game.game_state = GameState.from_dict(data["game_state"])

        return game

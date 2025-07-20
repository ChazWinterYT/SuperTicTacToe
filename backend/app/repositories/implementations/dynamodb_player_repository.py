import boto3
from typing import List, Optional
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError
from app.core.config import settings
from app.core.exceptions import NotFoundError, DatabaseError
from app.domain.entities.player import Player
from app.repositories.interfaces.player_repository import PlayerRepository


class DynamoDBPlayerRepository(PlayerRepository):
    """DynamoDB implementation of the player repository."""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name=settings.aws_region)
        self.table = self.dynamodb.Table(f"{settings.dynamodb_table_name}-Players")
    
    async def create(self, player: Player) -> Player:
        """Create a new player."""
        try:
            self.table.put_item(Item=player.to_dict())
            return player
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to create player: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error creating player: {str(e)}")
    
    async def get_by_id(self, player_id: str) -> Optional[Player]:
        """Get a player by ID."""
        try:
            response = self.table.get_item(Key={"player_id": player_id})
            if "Item" not in response:
                return None
            
            return Player.from_dict(response["Item"])
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get player by ID: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting player by ID: {str(e)}")
    
    async def get_by_name(self, name: str) -> Optional[Player]:
        """Get a player by name."""
        try:
            response = self.table.scan(
                FilterExpression="#player_name = :name",
                ExpressionAttributeNames={"#player_name": "name"},
                ExpressionAttributeValues={":name": name}
            )

            items = response.get("Items", [])
            if not items:
                return None

            return Player.from_dict(items[0])
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get player by name: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting player by name: {str(e)}")
    
    async def get_all_online(self) -> List[Player]:
        """Get all online players."""
        try:
            response = self.table.scan(
                FilterExpression="is_online = :is_online",
                ExpressionAttributeValues={":is_online": True}
            )
            
            return [Player.from_dict(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get online players: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting online players: {str(e)}")
    
    async def get_all_in_lobby(self) -> List[Player]:
        """Get all players currently in the lobby (not in a game)."""
        try:
            response = self.table.scan(
                FilterExpression="attribute_not_exists(current_game_id) AND is_online = :is_online",
                ExpressionAttributeValues={":is_online": True}
            )
            
            return [Player.from_dict(item) for item in response.get("Items", [])]
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to get lobby players: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error getting lobby players: {str(e)}")
    
    async def update(self, player: Player) -> Player:
        """Update a player."""
        try:
            # Update last_seen timestamp
            player.update_last_seen()
            
            self.table.put_item(Item=player.to_dict())
            return player
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to update player: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error updating player: {str(e)}")
    
    async def delete(self, player_id: str) -> bool:
        """Delete a player."""
        try:
            response = self.table.delete_item(Key={"player_id": player_id})
            return "Attributes" in response
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to delete player: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error deleting player: {str(e)}")
    
    async def mark_offline(self, player_id: str) -> bool:
        """Mark a player as offline."""
        try:
            player = await self.get_by_id(player_id)
            if not player:
                return False
            
            player.go_offline()
            await self.update(player)
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to mark player offline: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error marking player offline: {str(e)}")
    
    async def update_last_seen(self, player_id: str) -> bool:
        """Update a player's last seen timestamp."""
        try:
            player = await self.get_by_id(player_id)
            if not player:
                return False
            
            player.update_last_seen()
            await self.update(player)
            return True
        except (ClientError, NoCredentialsError, EndpointConnectionError) as e:
            raise DatabaseError(f"Failed to update last seen: {str(e)}")
        except Exception as e:
            raise DatabaseError(f"Unexpected error updating last seen: {str(e)}") 
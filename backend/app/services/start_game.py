import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Logic to create a new game
    game_id = create_new_game()  # Implement this function to create a game in DynamoDB

    # Optionally, send a dummy move to warm up the game move function
    send_dummy_move(game_id)

    return {
        'statusCode': 200,
        'body': json.dumps({'game_id': game_id})
    }

def create_new_game():
    # Implement the logic to create a new game in the DynamoDB table
    # Example:
    response = table.put_item(
        Item={
            'id': 'new_game_id',  # Generate a unique game ID
            'status': 'waiting',
            # Add other game attributes as needed
        }
    )
    return 'new_game_id'  # Return the created game ID

def send_dummy_move(game_id):
    # Implement logic to send a dummy move if needed
    pass

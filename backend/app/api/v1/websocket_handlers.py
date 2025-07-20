import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
connections_table_name = os.environ['CONNECTIONS_TABLE_NAME']
connections_table = dynamodb.Table(connections_table_name)

apigw_management_api = None

def get_apigw_management_api(event):
    global apigw_management_api
    if apigw_management_api is None:
        domain_name = event['requestContext']['domainName']
        stage = event['requestContext']['stage']
        endpoint_url = f"https://{domain_name}/{stage}"
        apigw_management_api = boto3.client('apigatewaymanagementapi', endpoint_url=endpoint_url)
    return apigw_management_api

def connect_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    # Optionally, authenticate the user here using headers or query params
    # Store the connection in DynamoDB
    connections_table.put_item(Item={'connection_id': connection_id})
    return {'statusCode': 200}

def disconnect_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    # Remove the connection from DynamoDB
    connections_table.delete_item(Key={'connection_id': connection_id})
    return {'statusCode': 200}

def message_handler(event, context):
    connection_id = event['requestContext']['connectionId']
    apigw_client = get_apigw_management_api(event)

    try:
        body = json.loads(event['body'])
        action = body.get('action')
        data = body.get('data')
    except Exception:
        return {'statusCode': 400, 'body': 'Invalid message format'}

    # Example: Broadcast message to all connected clients
    response = connections_table.scan()
    items = response.get('Items', [])

    for item in items:
        target_connection_id = item['connection_id']
        try:
            apigw_client.post_to_connection(
                Data=json.dumps({'action': action, 'data': data}),
                ConnectionId=target_connection_id
            )
        except apigw_client.exceptions.GoneException:
            # Connection no longer exists, remove from table
            connections_table.delete_item(Key={'connection_id': target_connection_id})

    return {'statusCode': 200}

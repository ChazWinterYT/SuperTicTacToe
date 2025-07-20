import pytest
import json
import os
from unittest.mock import patch, MagicMock

# Set environment variable for tests
os.environ['CONNECTIONS_TABLE_NAME'] = 'test-connections-table'

from app.api.v1 import websocket_handlers

@pytest.fixture
def mock_event_connect():
    return {
        'requestContext': {
            'connectionId': 'test-connection-id',
            'domainName': 'test-domain',
            'stage': 'test-stage'
        }
    }

@pytest.fixture
def mock_event_disconnect():
    return {
        'requestContext': {
            'connectionId': 'test-connection-id'
        }
    }

@pytest.fixture
def mock_event_message():
    return {
        'requestContext': {
            'connectionId': 'test-connection-id',
            'domainName': 'test-domain',
            'stage': 'test-stage'
        },
        'body': json.dumps({
            'action': 'sendMessage',
            'data': {'message': 'hello'}
        })
    }

@patch('app.api.v1.websocket_handlers.connections_table')
def test_connect_handler(mock_connections_table, mock_event_connect):
    mock_connections_table.put_item.return_value = {}
    response = websocket_handlers.connect_handler(mock_event_connect, None)
    mock_connections_table.put_item.assert_called_once_with(Item={'connection_id': 'test-connection-id'})
    assert response['statusCode'] == 200

@patch('app.api.v1.websocket_handlers.connections_table')
def test_disconnect_handler(mock_connections_table, mock_event_disconnect):
    mock_connections_table.delete_item.return_value = {}
    response = websocket_handlers.disconnect_handler(mock_event_disconnect, None)
    mock_connections_table.delete_item.assert_called_once_with(Key={'connection_id': 'test-connection-id'})
    assert response['statusCode'] == 200

@patch('app.api.v1.websocket_handlers.connections_table')
@patch('app.api.v1.websocket_handlers.boto3.client')
def test_message_handler(mock_boto3_client, mock_connections_table, mock_event_message):
    mock_connections_table.scan.return_value = {
        'Items': [{'connection_id': 'conn1'}, {'connection_id': 'conn2'}]
    }
    mock_apigw_client = MagicMock()
    mock_boto3_client.return_value = mock_apigw_client

    response = websocket_handlers.message_handler(mock_event_message, None)

    assert response['statusCode'] == 200
    assert mock_apigw_client.post_to_connection.call_count == 2
    mock_apigw_client.post_to_connection.assert_any_call(
        Data=json.dumps({'action': 'sendMessage', 'data': {'message': 'hello'}}),
        ConnectionId='conn1'
    )
    mock_apigw_client.post_to_connection.assert_any_call(
        Data=json.dumps({'action': 'sendMessage', 'data': {'message': 'hello'}}),
        ConnectionId='conn2'
    )

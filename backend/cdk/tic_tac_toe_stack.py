from aws_cdk import (
    App,
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as apigwv2_integrations,
    CfnOutput
)
from constructs import Construct

class TicTacToeStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define a standard prefix for DynamoDB table names
        table_name_prefix = "SuperTicTacToe"

        # Create DynamoDB table for games
        games_table = dynamodb.Table(
            self, "GamesTable",
            partition_key=dynamodb.Attribute(
                name="game_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{table_name_prefix}-games"
        )

        # Add GSI for querying games by player_id
        games_table.add_global_secondary_index(
            index_name="PlayerIdIndex",
            partition_key=dynamodb.Attribute(
                name="player_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="game_id",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL
        )

        # Create DynamoDB table for players
        players_table = dynamodb.Table(
            self, "PlayersTable",
            partition_key=dynamodb.Attribute(
                name="player_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{table_name_prefix}-players"
        )

        # Create DynamoDB table for WebSocket connections
        connections_table = dynamodb.Table(
            self, "ConnectionsTable",
            partition_key=dynamodb.Attribute(
                name="connection_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{table_name_prefix}-connections"
        )

        # Create Lambda function for the FastAPI app
        fastapi_lambda = _lambda.Function(
            self, "FastApiFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="main.lambda_handler",
            code=_lambda.Code.from_asset("app"),
            environment={
                "DYNAMODB_GAMES_TABLE_NAME": games_table.table_name,
                "DYNAMODB_PLAYERS_TABLE_NAME": players_table.table_name,
            }
        )

        # Grant Lambda permissions to access both DynamoDB tables
        games_table.grant_read_write_data(fastapi_lambda)
        players_table.grant_read_write_data(fastapi_lambda)

        # Create an HTTP API Gateway with Lambda proxy integration
        http_api = apigwv2.HttpApi(
            self, "FastApiHttpApi",
            default_integration=apigwv2_integrations.HttpLambdaIntegration(
                "FastApiLambdaIntegration",
                handler=fastapi_lambda
            )
        )

        # Output the API URL
        CfnOutput(
            self, "ApiUrl",
            value=http_api.api_endpoint
        )

        # Create Lambda functions for WebSocket API routes
        connect_lambda = _lambda.Function(
            self, "ConnectFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="websocket_handlers.connect_handler",
            code=_lambda.Code.from_asset("app"),
            environment={
                "CONNECTIONS_TABLE_NAME": connections_table.table_name,
            }
        )

        disconnect_lambda = _lambda.Function(
            self, "DisconnectFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="websocket_handlers.disconnect_handler",
            code=_lambda.Code.from_asset("app"),
            environment={
                "CONNECTIONS_TABLE_NAME": connections_table.table_name,
            }
        )

        message_lambda = _lambda.Function(
            self, "MessageFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="websocket_handlers.message_handler",
            code=_lambda.Code.from_asset("app"),
            environment={
                "CONNECTIONS_TABLE_NAME": connections_table.table_name,
            }
        )

        # Grant permissions to Lambda functions to access the connections table
        connections_table.grant_read_write_data(connect_lambda)
        connections_table.grant_read_write_data(disconnect_lambda)
        connections_table.grant_read_write_data(message_lambda)

        # Create WebSocket API
        websocket_api = apigwv2.WebSocketApi(
            self, "WebSocketApi",
            connect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2_integrations.WebSocketLambdaIntegration(
                    "ConnectIntegration",
                    handler=connect_lambda
                )
            ),
            disconnect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2_integrations.WebSocketLambdaIntegration(
                    "DisconnectIntegration",
                    handler=disconnect_lambda
                )
            )
        )

        # Add a custom route for messages
        websocket_api.add_route(
            "sendMessage",
            integration=apigwv2_integrations.WebSocketLambdaIntegration(
                "MessageIntegration",
                handler=message_lambda
            )
        )

        # Create a stage for the WebSocket API
        websocket_stage = apigwv2.WebSocketStage(
            self, "WebSocketStage",
            web_socket_api=websocket_api,
            stage_name="prod",
            auto_deploy=True
        )

        # Output the WebSocket API endpoint
        CfnOutput(
            self, "WebSocketApiUrl",
            value=websocket_stage.url
        )

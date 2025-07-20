from aws_cdk import (
    App,
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as apigwv2_integrations,
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

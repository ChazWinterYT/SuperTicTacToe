from aws_cdk import (
    App,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class TicTacToeStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a DynamoDB table for games
        game_table = dynamodb.Table(
            self, "GameTable",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Create a Lambda function for starting a new game
        start_game_function = _lambda.Function(
            self, "StartGameFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="game_service.lambda_handler",
            code=_lambda.Code.from_asset("app/services"),
            environment={
                "DYNAMODB_TABLE_NAME": game_table.table_name,
            }
        )

        # Grant the Lambda function permissions to read/write to the DynamoDB table
        game_table.grant_read_write_data(start_game_function)

        # Create an API Gateway
        api = apigateway.RestApi(self, "TicTacToeAPI")

        # Create a resource for starting a game
        start_game_resource = api.root.add_resource("start")
        start_game_resource.add_method("POST", apigateway.LambdaIntegration(start_game_function))

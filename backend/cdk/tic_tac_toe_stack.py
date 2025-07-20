from aws_cdk import (
    App, Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as apigwv2_integrations,
    aws_iam as iam,
    CfnOutput, Fn
)
from constructs import Construct


class TicTacToeStack(Stack):
    def __init__(self, scope: Construct, id_: str, **kwargs) -> None:
        super().__init__(scope, id_, **kwargs)

        # ─────────────────── DynamoDB ───────────────────
        prefix = "SuperTicTacToe"

        games_table = dynamodb.Table(
            self, "Games",
            partition_key=dynamodb.Attribute(name="game_id",
                                             type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{prefix}-games",
        )
        games_table.add_global_secondary_index(
            index_name="PlayerIdIndex",
            partition_key=dynamodb.Attribute(name="player_id",
                                             type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="game_id",
                                        type=dynamodb.AttributeType.STRING),
            projection_type=dynamodb.ProjectionType.ALL,
        )

        players_table = dynamodb.Table(
            self, "Players",
            partition_key=dynamodb.Attribute(name="player_id",
                                             type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{prefix}-players",
        )

        connections_table = dynamodb.Table(
            self, "Connections",
            partition_key=dynamodb.Attribute(name="connection_id",
                                             type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            table_name=f"{prefix}-connections",
        )

        # ─────────────────── REST  (HttpApi) ───────────────────
        fastapi_lambda = _lambda.Function(
            self, "FastApi",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="main.lambda_handler",
            code=_lambda.Code.from_asset("app"),
            environment={
                "DYNAMODB_GAMES_TABLE_NAME": games_table.table_name,
                "DYNAMODB_PLAYERS_TABLE_NAME": players_table.table_name,
            },
        )
        games_table.grant_read_write_data(fastapi_lambda)
        players_table.grant_read_write_data(fastapi_lambda)

        http_api = apigwv2.HttpApi(
            self, "HttpApi",
            default_integration=apigwv2_integrations.HttpLambdaIntegration(
                "FastApiIntegration", fastapi_lambda
            ),
        )
        CfnOutput(self, "RestApiUrl", value=http_api.api_endpoint)

        # ─────────────────── WebSocket API ───────────────────
        def ws_lambda(id_: str, handler: str):
            fn = _lambda.Function(
                self, id_,
                runtime=_lambda.Runtime.PYTHON_3_11,
                handler=f"websocket_handlers.{handler}",
                code=_lambda.Code.from_asset("app"),
                environment={
                    "CONNECTIONS_TABLE_NAME": connections_table.table_name,
                },
            )
            connections_table.grant_read_write_data(fn)
            return fn

        connect_fn = ws_lambda("ConnectFn", "connect_handler")
        disconnect_fn = ws_lambda("DisconnectFn", "disconnect_handler")
        message_fn = ws_lambda("MessageFn", "message_handler")

        websocket_api = apigwv2.WebSocketApi(
            self, "WebSocketApi",
            connect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2_integrations.WebSocketLambdaIntegration(
                    "ConnectIntegration", connect_fn)),
            disconnect_route_options=apigwv2.WebSocketRouteOptions(
                integration=apigwv2_integrations.WebSocketLambdaIntegration(
                    "DisconnectIntegration", disconnect_fn)),
        )
        websocket_api.add_route(
            "sendMessage",
            integration=apigwv2_integrations.WebSocketLambdaIntegration(
                "MessageIntegration", message_fn),
        )

        websocket_stage = apigwv2.WebSocketStage(
            self, "ProdStage",
            web_socket_api=websocket_api,
            stage_name="prod",
            auto_deploy=True,
        )
        CfnOutput(self, "WebSocketWssUrl", value=websocket_stage.url)

        # ─────── Derived HTTPS management URL and env-vars ───────
        mgmt_url = Fn.join(
            "",
            [
                "https://",
                websocket_api.api_endpoint,
                "/",
                websocket_stage.stage_name,
                "/@connections",
            ],
        )

        for fn in (connect_fn, disconnect_fn, message_fn, fastapi_lambda):
            fn.add_environment("WEBSOCKET_MGMT_URL", mgmt_url)

        # ───────── Give Lambdas permission to call post_to_connection ─────────
        for fn in (connect_fn, disconnect_fn, message_fn):
            fn.add_to_role_policy(
                iam.PolicyStatement(
                    actions=["execute-api:ManageConnections"],
                    resources=[f"arn:{self.partition}:execute-api:{self.region}:{self.account}:{websocket_api.api_id}/{websocket_stage.stage_name}/POST/@connections/*"],
                )
            )

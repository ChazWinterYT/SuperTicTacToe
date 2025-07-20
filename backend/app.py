from aws_cdk import App
from cdk.tic_tac_toe_stack import TicTacToeStack

app = App()
TicTacToeStack(app, "TicTacToeStack")
app.synth()
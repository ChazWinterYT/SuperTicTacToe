from fastapi import FastAPI
from mangum import Mangum
from . import lobby, websocket

app = FastAPI()

app.include_router(websocket.router, prefix="/ws")
app.include_router(lobby.router, prefix="/lobby")

@app.get("/")
def read_root():
    """This doesn't work. Eh, who cares."""
    return {
        "message": "This is the Tac Tac Toe API."
    }

# AWS Lambda Handler
lambda_handler = Mangum(app)

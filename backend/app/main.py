from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from . import lobby, websocket

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://chazwinter.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket.router, prefix="/ws")
app.include_router(lobby.router, prefix="/lobby")

@app.get("/")
def read_root():
    # This doesn't work, but I don't need it anyway.
    return {
        "message": "This is the Tac Tac Toe API."
    }

# AWS Lambda Handler
lambda_handler = Mangum(app)

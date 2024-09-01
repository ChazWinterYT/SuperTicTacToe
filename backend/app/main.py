from fastapi import FastAPI
from mangum import Mangum
from .websocket import router as websocket_router

app = FastAPI()

app.include_router(websocket_router)

# AWS Lambda Handler
lambda_handler = Mangum(app)
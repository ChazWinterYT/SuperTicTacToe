from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.core.config import settings
from app.core.exceptions import SuperTicTacToeException, handle_super_tictactoe_exception
from app.api.v1 import lobby, games, websocket


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add exception handlers
    app.add_exception_handler(
        SuperTicTacToeException,
        lambda request, exc: handle_super_tictactoe_exception(exc)
    )
    
    # Include API routers
    app.include_router(lobby.router, prefix=f"{settings.api_v1_prefix}/lobby", tags=["lobby"])
    app.include_router(games.router, prefix=f"{settings.api_v1_prefix}/games", tags=["games"])
    app.include_router(websocket.router, prefix=f"{settings.api_v1_prefix}/ws", tags=["websocket"])
    
    return app


# Create the application instance
app = create_app()


@app.get("/")
async def read_root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


# AWS Lambda Handler
lambda_handler = Mangum(app)

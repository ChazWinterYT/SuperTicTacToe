from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.core.config import settings
from app.core.exceptions import SuperTicTacToeException, handle_super_tictactoe_exception
from app.api.v1 import lobby, games

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from fastapi.responses import JSONResponse

    @app.exception_handler(SuperTicTacToeException)
    async def _handle(request, exc: SuperTicTacToeException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
            headers={
                "Access-Control-Allow-Origin": "https://chazwinter.com",
                "Access-Control-Allow-Credentials": "true",
            },
        )

    app.include_router(lobby.router,
                       prefix=f"{settings.api_v1_prefix}/lobby",
                       tags=["lobby"])
    app.include_router(games.router,
                       prefix=f"{settings.api_v1_prefix}/games",
                       tags=["games"])

    @app.get("/")
    async def root():
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": settings.app_version}

    return app


app = create_app()
lambda_handler = Mangum(app)

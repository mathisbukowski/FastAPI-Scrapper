from fastapi import FastAPI

from .core.config import settings
from .graphql_app.router import graphql_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(graphql_router, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "graphql": "/graphql"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=int(settings.PORT)
    )

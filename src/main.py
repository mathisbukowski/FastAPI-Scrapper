from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
import os
from pathlib import Path

from .core.config import settings
from .core.database import Base, engine
from alembic import command
from alembic.config import Config as AlembicConfig
from . import models  # noqa: F401 ensures models imported
from .graphql.router import graphql_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan: initialize database tables at startup.
    Ensures all SQLAlchemy models are imported so Base.metadata is complete,
    then creates missing tables.
    """

    logger = logging.getLogger("startup")
    logger.info("Starting application lifespan: applying migrations")
    try:
        project_root = Path(__file__).resolve().parent.parent
        alembic_cfg = AlembicConfig(str(project_root / "alembic.ini"))
        os.environ.setdefault("DATABASE_URL", settings.database_url)
        logger.info("Running Alembic upgrade head...")
        command.upgrade(alembic_cfg, "head")
        logger.info("Alembic upgrade completed.")
    except Exception as exc:
        logger.error(f"Alembic upgrade failed: {exc}. Falling back to create_all().")
        Base.metadata.create_all(bind=engine)
        logger.info("Fallback create_all complete.")
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(graphql_router, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "graphql": "/graphql",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.HOST,
        port=int(settings.PORT),
    )

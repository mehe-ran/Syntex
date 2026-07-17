from contextlib import asynccontextmanager
from fastapi import FastAPI
from syntex.core.config import settings
from syntex.core.logger import logger
from syntex.api.routes import router as api_router

# manage startup and shutdown events cleanly
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"starting {settings.app_name} (debug={settings.debug_mode})")
    # future: initialize vector db connection here
    yield
    logger.info(f"shutting down {settings.app_name}")
    # future: close database connections cleanly here

# initialize fastapi application
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

# mount the api routes under a versioned prefix
app.include_router(api_router, prefix="/api/v1")

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from syntex.core.config import settings
from syntex.core.logger import logger
from syntex.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"starting {settings.app_name} (debug={settings.debug_mode})")
    yield
    logger.info(f"shutting down {settings.app_name}")

# initialize fastapi application
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan
)

# configure cors for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount the api routes under a versioned prefix
app.include_router(api_router, prefix="/api/v1")

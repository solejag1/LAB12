"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth import router as auth_router
from app.api.v1.accounts import router as accounts_router
from app.api.v1.cards import router as cards_router
from app.api.v1.history import router as history_router
from app.api.v1.transfers import transfers_router, payments_router
from app.core.config import settings
from app.core.dependencies import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all tables on startup (development convenience)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"
app.include_router(auth_router, prefix=PREFIX)
app.include_router(accounts_router, prefix=PREFIX)
app.include_router(cards_router, prefix=PREFIX)
app.include_router(transfers_router, prefix=PREFIX)
app.include_router(payments_router, prefix=PREFIX)
app.include_router(history_router, prefix=PREFIX)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.APP_NAME}

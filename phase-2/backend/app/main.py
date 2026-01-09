"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.routes import health
from app.api.routes import tasks, tasks_extended, tags, reminders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Close database connections
    await close_db()


app = FastAPI(
    title="Todo API",
    description="RESTful API for managing todo tasks",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend - place this first to ensure it applies to all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Add this to ensure CORS headers are applied even to error responses
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):[0-9]+",
)




# Include routers
app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(tasks_extended.router)
app.include_router(tags.router)
app.include_router(reminders.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
    }



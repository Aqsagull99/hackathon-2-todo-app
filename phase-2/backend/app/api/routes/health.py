"""Health check endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns service status for monitoring and load balancers.
    """
    return HealthResponse(
        status="healthy",
        message="Todo API is running",
    )

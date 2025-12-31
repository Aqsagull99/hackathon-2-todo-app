"""API dependencies."""

from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import get_current_user, verify_user_access


# Type aliases for cleaner route signatures
DBSession = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[dict, Depends(get_current_user)]


async def get_verified_user_id(
    user_id: str = Path(..., description="User ID"),
    current_user: dict = Depends(get_current_user),
) -> str:
    """Dependency that verifies user has access to the requested user_id.

    Args:
        user_id: User ID from path
        current_user: Current authenticated user

    Returns:
        Verified user ID
    """
    return await verify_user_access(user_id, current_user)


VerifiedUserId = Annotated[str, Depends(get_verified_user_id)]

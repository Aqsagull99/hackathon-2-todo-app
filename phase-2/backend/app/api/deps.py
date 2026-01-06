"""API dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, Path
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


async def get_current_user_id(
    current_user: dict = Depends(get_current_user),
) -> str:
    """Dependency that gets the current user ID directly from JWT token.

    Args:
        current_user: Current authenticated user from JWT

    Returns:
        Current user ID
    """
    # Get user ID from JWT payload (Better Auth uses 'sub' for user ID)
    user_id = current_user.get("sub") or current_user.get("userId")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id


VerifiedUserId = Annotated[str, Depends(get_verified_user_id)]
VerifiedUserIdFromToken = Annotated[str, Depends(get_current_user_id)]



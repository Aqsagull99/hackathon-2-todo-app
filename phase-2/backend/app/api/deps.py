"""API dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
import logging
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
    return await verify_user_access(user_id, current_user=current_user)


async def get_current_user_id(
    current_user: dict = Depends(get_current_user),
) -> str:
    """Dependency that gets the current user ID directly from JWT token.

    Args:
        current_user: Current authenticated user from JWT

    Returns:
        Current user ID
    """
    # Get possible user identifier from JWT (Better Auth uses 'sub')
    user_identifier = current_user.get("sub") or current_user.get("userId")

    # If the token contains a UUID-like identifier, return it directly
    if user_identifier:
        try:
            from uuid import UUID

            UUID(user_identifier)
            logger = logging.getLogger(__name__)
            logger.info("[auth] Using UUID from token: %s", user_identifier)
            return user_identifier
        except Exception:
            # Not a valid UUID, fall through to email-based mapping
            logger = logging.getLogger(__name__)
            logger.info("[auth] Token identifier not a UUID: %s", user_identifier)
            pass

    # Fallback: map by email claim in the JWT. Create user if missing.
    email = current_user.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User identity not found in token (no UUID and no email)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from app.core.database import async_session_maker
    from app.models.user import User
    from sqlmodel import select
    from uuid import uuid4

    async with async_session_maker() as session:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            # Create a new user with a UUID primary key
            new_id = uuid4()
            user = User(id=new_id, email=email, name=current_user.get("name") or "Default User")
            session.add(user)
            await session.commit()
            await session.refresh(user)

        logger = logging.getLogger(__name__)
        logger.info("[auth] Mapped token email %s -> user id %s", email, user.id)

        return str(user.id)


VerifiedUserId = Annotated[str, Depends(get_verified_user_id)]
VerifiedUserIdFromToken = Annotated[str, Depends(get_current_user_id)]



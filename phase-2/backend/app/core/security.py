"""JWT verification for Better Auth tokens."""

from datetime import datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.core.config import settings


# HTTP Bearer scheme for JWT tokens
security = HTTPBearer()


def verify_jwt(token: str) -> Optional[dict]:
    """Verify JWT token and return payload.

    Args:
        token: JWT token string

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Dependency to get current authenticated user from JWT.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        User payload from JWT

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = verify_jwt(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check token expiration
    exp = payload.get("exp")
    if exp and datetime.utcnow().timestamp() > exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def verify_user_access(
    user_id: str,
    current_user: dict = Depends(get_current_user),
) -> str:
    """Verify that current user has access to the requested user_id.

    Args:
        user_id: The user ID from path parameter
        current_user: Current authenticated user from JWT

    Returns:
        The verified user_id

    Raises:
        HTTPException: If user doesn't have access
    """
    # Get user ID from JWT payload (Better Auth uses 'sub' for user ID)
    jwt_user_id = current_user.get("sub") or current_user.get("userId")

    if jwt_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource",
        )

    return user_id

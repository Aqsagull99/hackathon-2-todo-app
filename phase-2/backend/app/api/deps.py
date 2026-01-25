from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_session

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    credentials_exception_msg = "Could not validate credentials"
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"leeway": 3600}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return user_id
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

CurrentUser = Annotated[str, Depends(get_current_user)]

# Database session dependency
DBSession = Annotated[AsyncSession, Depends(get_session)]

# Verified user ID dependency (same as CurrentUser)
VerifiedUserId = Annotated[str, Depends(get_current_user)]

# Alternative name for the same functionality
VerifiedUserIdFromToken = Annotated[str, Depends(get_current_user)]

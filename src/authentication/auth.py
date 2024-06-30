from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.auth_utils import (decode_access_token,
                                           is_token_blacklisted)
from src.database.db import get_session
from src.user_module.services import user_service

security = HTTPBearer()


async def token_manager(token: str = Depends(security)) -> Optional[dict]:
    """
    Validate and decode the JWT token to extract the payload.

    Args:
        token (str): The JWT token passed as a dependency from the security module.

    Returns:
        Optional[dict]: The decoded token payload if the token is valid.

    Raises:
        HTTPException: If the token is invalid, token blacklisted, or a refresh token is provided instead of an access token.
    """
    try:
        token = token.credentials
        decode_token_payload = decode_access_token(token)
        if not decode_token_payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        if decode_token_payload.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Provide an access token"
            )
        if is_token_blacklisted(jti=decode_token_payload.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has been blacklisted. Log in again.",
            )

        return decode_token_payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


async def get_current_active_user(
    token_manager: dict = Depends(token_manager),
    session: AsyncSession = Depends(get_session),
) -> Optional[dict]:
    """
    Retrieve the current active user from the database using the token payload.

    Args:
        user_service (UserService): The user service class instance.
        token_manager (dict): The token payload containing the user and token information.
        session (AsyncSession): The database session passed as a dependency.

    Returns:
        Optional[dict]: The user information if the user exists and is active.

    Raises:
        HTTPException: If the user is not found or is inactive.
    """

    try:
        user_uid = token_manager.get("sub")
        user = await user_service.retrieve_user(user_uid, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

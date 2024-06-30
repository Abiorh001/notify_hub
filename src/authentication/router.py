from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_session

from .auth import token_manager
from .schema import (UserLoginResponse, UserLoginSchema,
                     UserRefreshAccessTokenResponse,
                     UserRefreshAccessTokenSchema)
from .service import AuthenticationService

auth_router = APIRouter(prefix="/auth", tags=["authentication"])


@auth_router.post("/login/", response_model=UserLoginResponse)
async def login_user(
    user_payload: UserLoginSchema,
    session: AsyncSession = Depends(get_session),
    auth_service: AuthenticationService = Depends(AuthenticationService),
):
    user_login = await auth_service.login_user(user_payload, session)
    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email or password is incorrect",
        )
    return user_login


@auth_router.post(
    "/refresh/",
    status_code=status.HTTP_200_OK,
)
async def refresh_access_token(
    refresh_token_payload: UserRefreshAccessTokenSchema,
    auth_service: AuthenticationService = Depends(AuthenticationService),
    token_manager: dict = Depends(token_manager),
) -> Optional[UserRefreshAccessTokenResponse]:
    try:
        new_access_token = await auth_service.generate_new_access_token(
            refresh_token_payload.refresh_token
        )
        if not new_access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid refresh token"
            )
        return new_access_token
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/logout/", status_code=status.HTTP_200_OK)
async def log_out_user(
    auth_service: AuthenticationService = Depends(AuthenticationService),
    token_manager: dict = Depends(token_manager),
) -> JSONResponse:
    try:
        jti = token_manager.get("jti")
        if not jti:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token"
            )
        blacklisted = await auth_service.log_out_user(jti)
        if not blacklisted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token not blacklisted"
            )
        return JSONResponse(
            content={
                "message": "User logged out successfully",
                "status": "success",
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

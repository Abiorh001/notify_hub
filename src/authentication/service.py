from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.user_module.model import User

from .auth_utils import (blacklist_token_jti, create_access_token,
                         create_refresh_token, refresh_access_token,
                         verify_password)
from .schema import (UserLoginResponse, UserLoginSchema,
                     UserRefreshAccessTokenResponse,
                     UserRefreshAccessTokenSchema)


class AuthenticationService:
    async def login_user(
        self, user_login_schema: UserLoginSchema, session: AsyncSession
    ) -> Optional[UserLoginResponse]:
        statement = select(User).where(User.email == user_login_schema.email)
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            return None
        if not verify_password(user_login_schema.password, user.password):
            return None
        user_claim = {"sub": str(user.uid)}
        access_token = create_access_token(payload=user_claim)
        refresh_token = create_refresh_token(payload=user_claim)
        user_response = UserLoginResponse(
            uid=user.uid,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            role_uid=user.role_uid,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
        return user_response

    async def generate_new_access_token(
        self, refresh_token_schema: UserRefreshAccessTokenSchema
    ) -> Optional[UserRefreshAccessTokenResponse]:
        new_access_token = refresh_access_token(refresh_token_schema)
        if not new_access_token:
            return None
        user_response = UserRefreshAccessTokenResponse(
            access_token=new_access_token,
            token_type="bearer",
        )
        return user_response

    async def log_out_user(self, token_jti: str) -> bool:
        blacklist_jti = await blacklist_token_jti(token_jti)
        if not blacklist_jti:
            return False
        return True

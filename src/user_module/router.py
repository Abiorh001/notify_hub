from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.auth import get_current_active_user, token_manager
from src.database.db import get_session

from .schema import UserResponse, UserSchema, UserUpdateSchema
from .services import UserService

user_module_router = APIRouter(prefix="/users", tags=["User Management"])


@user_module_router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_user(
    user_payload: UserSchema,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
):

    try:
        user_response = await user_service.create_user(user_payload, session)
        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not created"
            )
        return user_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_module_router.get("/profile", response_model=UserResponse)
async def retrieve_user_by_token(
    current_active_user: UserResponse = Depends(get_current_active_user),
):

    try:
        user_response = current_active_user
        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_module_router.get("/", response_model=UserResponse)
async def retrieve_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    current_active_user: UserResponse = Depends(get_current_active_user),
):

    user_response = await user_service.get_user_by_email(email, session)
    if not user_response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user_response


@user_module_router.patch(
    "/", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    user_payload: UserUpdateSchema,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    current_active_user: UserResponse = Depends(get_current_active_user),
):

    try:
        user_uid = current_active_user.uid
        user_response = await user_service.update_user(
            user_uid=user_uid, user_update_schema=user_payload, session=session
        )
        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not updated"
            )
        return user_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@user_module_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    current_active_user: UserResponse = Depends(get_current_active_user),
):

    try:
        user_uid = current_active_user.uid
        await user_service.delete_user(user_uid, session)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(
        content={"message": "User deleted successfully", "status": "success"},
        status_code=status.HTTP_204_NO_CONTENT,
    )

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.authentication.auth import AdminRoleChecker, get_current_active_user
from src.database.db import get_session

from .schema import (RoleResponse, RoleSchema, UserResponse, UserRoleSchema,
                     UserSchema, UserUpdateSchema)
from .services import RoleService, UserService

user_module_router = APIRouter(prefix="/users", tags=["User Management"])

admin_role = AdminRoleChecker()


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@user_module_router.get(
    "/profile", response_model=UserResponse, status_code=status.HTTP_200_OK
)
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@user_module_router.get("/", response_model=UserResponse)
async def retrieve_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    current_active_user: UserResponse = Depends(
        get_current_active_user
    ),  # pylint: disable=unused-argument
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    return JSONResponse(
        content={"message": "User deleted successfully", "status": "success"},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@user_module_router.post(
    "/roles", response_model=RoleResponse, dependencies=[Depends(admin_role)]
)
async def create_new_role(
    role_payload: RoleSchema,
    session: AsyncSession = Depends(get_session),
    role_service: RoleService = Depends(RoleService),
    current_active_user: UserResponse = Depends(
        get_current_active_user
    ),  # pylint: disable=unused-argument
):

    try:
        role_response = await role_service.create_new_role(role_payload, session)
        if not role_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role not created"
            )
        return role_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@user_module_router.patch(
    "/assign-user-role/",
    response_model=UserResponse,
    dependencies=[Depends(admin_role)],
)
async def assign_user_role(
    user_role_payload: UserRoleSchema,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(UserService),
    current_active_user: UserResponse = Depends(
        get_current_active_user
    ),  # pylint: disable=unused-argument
) -> UserResponse:

    try:
        user_response = await user_service.assign_role_to_use(
            user_role_payload, session
        )
        if not user_response:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User role not assigned"
            )
        return user_response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e

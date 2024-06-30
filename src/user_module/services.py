from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.authentication.auth_utils import get_password_hash, verify_password

from .model import Role, User
from .schema import (RoleResponse, RoleSchema, UserResponse, UserRoleSchema,
                     UserSchema, UserUpdateSchema)


class RoleService:
    async def create_new_role(
        self, role_schema: RoleSchema, session: AsyncSession
    ) -> Optional[RoleResponse]:
        try:

            role_schema = role_schema.model_dump()
            new_role = Role(**role_schema)
            session.add(new_role)
            await session.commit()
            await session.refresh(new_role)
            role_response = RoleResponse(
                uid=new_role.uid,
                role=new_role.role,
                description=new_role.description,
                permissions=new_role.permissions,
            )
            return role_response
        except IntegrityError as e:
            await session.rollback()
            raise e.orig
        except Exception as e:
            await session.rollback()
            raise e

    async def retrieve_role_by_uuid(
        self, role_uid: str, session: AsyncSession
    ) -> Optional[RoleResponse]:
        role = await session.get(Role, role_uid)
        if not role:
            return None
        role_response = RoleResponse(
            uid=role.uid,
            role=role.role,
            description=role.description,
            permissions=role.permissions,
        )
        return role_response


role_service = RoleService()


class UserService:
    """
    Service class for user-related operations such as creating, retrieving, and searching users.
    """

    async def create_user(
        self, new_user_schema: UserSchema, session: AsyncSession
    ) -> Optional[UserResponse]:
        """
        Create a new user in the database.

        Args:
            new_user_schema (UserSchema): The schema containing new user data.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Optional[UserResponse]: The created user's response model.

        Raises:
            IntegrityError: If there is a uniqueness constraint violation (e.g., duplicate email).
            Exception: For any other errors that occur during the creation process.
        """
        try:
            new_user_schema.password = get_password_hash(new_user_schema.password)
            new_user_data = new_user_schema.model_dump()
            new_user = User(**new_user_data)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            user_response = UserResponse(
                uid=new_user.uid,
                first_name=new_user.first_name,
                last_name=new_user.last_name,
                email=new_user.email,
                is_active=new_user.is_active,
                role_uid=new_user.role_uid,
            )
            return user_response
        except IntegrityError as e:
            await session.rollback()
            raise e.orig
        except Exception as e:
            await session.rollback()
            raise e

    async def retrieve_user(
        self, user_uid: str, session: AsyncSession
    ) -> Optional[UserResponse]:
        """
        Retrieve a user by their UID.

        Args:
            user_uid (str): The UID of the user to retrieve.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Optional[UserResponse]: The retrieved user's response model, or None if not found.
        """
        user = await session.get(User, user_uid)
        if not user:
            return None
        user_response = UserResponse(
            uid=user.uid,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            role_uid=user.role_uid,
        )
        return user_response

    async def get_user_by_email(
        self, email: str, session: AsyncSession
    ) -> Optional[UserResponse]:
        """
        Retrieve a user by their email.

        Args:
            email (str): The email of the user to retrieve.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Optional[UserResponse]: The retrieved user's response model, or None if not found.
        """
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalars().first()
        if user:
            user_response = UserResponse(
                uid=user.uid,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
                role_uid=user.role_uid,
            )
            return user_response
        return None

    async def update_user(
        self, user_uid: str, user_update_schema: UserUpdateSchema, session: AsyncSession
    ) -> Optional[UserResponse]:
        """
        Update a user in the database.

        Args:
            user_uid (str): The UID of the user to update.
            user_update_schema (UserUpdateSchema): The schema containing updated user data.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Optional[UserResponse]: The updated user's response model.

        Raises:
            IntegrityError: If there is a uniqueness constraint violation (e.g., duplicate email).
            Exception: For any other errors that occur during the update process.
        """
        try:
            user = await session.get(User, user_uid)
            if not user:
                return None
            user_data = user_update_schema.model_dump()
            for attribute, new_value in user_data.items():
                if new_value is not None:
                    if attribute == "password":
                        password = new_value
                        if verify_password(password, user.password):
                            raise ValueError(
                                "New password must be different from the current password"
                            )
                        new_value = get_password_hash(password)
                    setattr(user, attribute, new_value)
            await session.commit()
            await session.refresh(user)
            user_response = UserResponse(
                uid=user.uid,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
                role_uid=user.role_uid,
            )
            return user_response
        except IntegrityError as e:
            await session.rollback()
            raise e.orig
        except Exception as e:
            await session.rollback()
            raise e

    async def delete_user(
        self, user_uid: str, session: AsyncSession
    ) -> Optional[UserResponse]:
        """
        Delete a user from the database.

        Args:
            user_uid (str): The UID of the user to delete.
            session (AsyncSession): The database session used for the operation.

        Returns:
            Optional[UserResponse]: The deleted user's response model.

        Raises:
            Exception: For any errors that occur during the deletion process.
        """
        try:
            user = await session.get(User, user_uid)
            if not user:
                return None
            await session.delete(user)
            await session.commit()
            user_response = UserResponse(
                uid=user.uid,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
                role_uid=user.role_uid,
            )
            return user_response
        except Exception as e:
            await session.rollback()
            raise e

    async def assign_role_to_use(
        self, user_role_schema: UserRoleSchema, session: AsyncSession
    ) -> Optional[UserResponse]:
        role = await role_service.retrieve_role_by_uuid(
            user_role_schema.role_uid, session
        )
        if not role:
            return None
        user = await session.get(User, user_role_schema.user_uid)
        if not user:
            return None
        user.role_uid = role.uid
        await session.commit()
        await session.refresh(user)
        user_response = UserResponse(
            uid=user.uid,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            role_uid=user.role_uid,
        )
        return user_response


user_service = UserService()

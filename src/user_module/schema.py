from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, validate_email


class UserSchema(BaseModel):
    password: str = Field(..., min_length=8, max_length=100)
    email: str = Field(..., min_length=6, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)

    @field_validator("email")
    def validate_email(cls, value):
        value = validate_email(value)
        return value[1]

    class Config:
        extra = "forbid"


class UserResponse(BaseModel):
    uid: UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    role_uid: Optional[UUID]


class UserUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, min_length=6, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

    @field_validator("email")
    def validate_email(cls, value):
        value = validate_email(value)
        return value[1]

    class Config:
        extra = "forbid"


class UserRoleSchema(BaseModel):
    role_uid: UUID
    user_uid: UUID

    class Config:
        extra = "forbid"


class RoleSchema(BaseModel):
    role: str = Field(..., min_length=2, max_length=100)
    permissions: list[str]
    description: str = Field(..., min_length=2, max_length=200)

    class Config:
        extra = "forbid"


class RoleResponse(BaseModel):
    uid: UUID
    role: str
    permissions: list[str]
    description: str

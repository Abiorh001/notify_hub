from uuid import UUID

from pydantic import BaseModel, Field, field_validator, validate_email


class UserLoginSchema(BaseModel):
    email: str = Field(..., min_length=6, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

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
    role_uid: UUID


class UserLoginResponse(BaseModel):
    uid: UUID
    email: str
    first_name: str
    last_name: str
    is_active: bool
    access_token: str
    refresh_token: str
    token_type: str


class UserRefreshAccessTokenSchema(BaseModel):
    refresh_token: str = Field(..., min_length=50, max_length=500)

    class Config:
        extra = "forbid"


class UserRefreshAccessTokenResponse(BaseModel):
    access_token: str
    token_type: str

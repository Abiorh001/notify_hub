from pydantic import BaseModel, Field, field_validator
from enum import Enum
from uuid import UUID, uuid4


class User(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    email: str = Field(..., min_length=5, max_length=50)
    is_active: bool = Field(default=True)


class UserResponse(BaseModel):
    username: str
    email: str
    is_active: bool
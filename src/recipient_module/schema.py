from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional


class RecipientSchema(BaseModel):
    first_name: str = Field(..., description="first name")
    last_name: str = Field(None, description="last name")
    email: str = Field(None, description="email address")
    phone_number: str = Field(None, description="phone number")
    created_by: UUID = Field(
        None, description="uuid of the user that create the new recipient"
    )


class RecipientResponse(BaseModel):
    uid: UUID
    first_name: str
    last_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
    created_by: UUID


class RecipientUpdateSchema(BaseModel):
    first_name: str = Field(None, description="first name")
    last_name: str = Field(None, description="last name")
    email: str = Field(None, description="email address")
    phone_number: str = Field(None, description="phone number")

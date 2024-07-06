from pydantic import BaseModel, Field
from uuid import UUID


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
    last_name: str
    email: str
    phone_number: str
    created_by: UUID


class RecipientUpdateSchema(BaseModel):
    first_name: str = Field(None, description="first name")
    last_name: str = Field(None, description="last name")
    email: str = Field(None, description="email address")
    phone_number: str = Field(None, description="phone number")

from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, SQLModel


class Recipient(SQLModel, table=True):
    __tablename__ = "recipeints"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=lambda: uuid4(), index=True)
    )
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100, nullable=True)
    email: str = Field(max_length=100,  nullable=True)
    phone_number: str = Field(max_length=30, nullable=True)
    created_by: UUID = Field(sa_column=Column(pg.UUID))

    def __str__(self):
        return self.uid

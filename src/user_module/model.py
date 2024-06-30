from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=lambda: uuid4(), index=True)
    )
    role: str = Field(..., min_length=2, max_length=100, unique=True)
    permissions: list[str] = Field(
        sa_column=Column(pg.ARRAY(pg.VARCHAR(100)), nullable=True)
    )
    description: str = Field(sa_column=Column(pg.TEXT, nullable=True))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    users: Optional[list["User"]] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=lambda: uuid4(), index=True)
    )
    password: str = Field(..., min_length=16, max_length=150)
    email: str = Field(..., min_length=5, max_length=150, unique=True)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    role_uid: Optional[UUID] = Field(default=None, foreign_key="roles.uid")
    role: Optional[Role] = Relationship(back_populates="users")

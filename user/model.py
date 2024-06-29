from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime


class Base(SQLModel):
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now()))


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid4())
    )
    username: str = Field(..., min_length=6, max_length=150)
    password: str = Field(..., min_length=16, max_length=150)
    email: str = Field(..., min_length=5, max_length=150)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: datetime = Field(Column(pg.TIMESTAMP, default=datetime.now()))
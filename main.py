from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import db_init


@asynccontextmanager
async def db_connection(app: FastAPI):
    print("Opening database connection")
    await db_init()
    yield
    print("Closing database connection")


app = FastAPI(lifespan=db_connection)

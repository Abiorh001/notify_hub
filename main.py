from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.authentication.router import auth_router
from src.database.db import db_init
from src.recipient_module.router import recipient_router
from src.user_module.router import user_module_router


@asynccontextmanager
async def db_connection(app: FastAPI):
    print("Opening database connection")
    await db_init()
    yield
    print("Closing database connection")


app = FastAPI(lifespan=db_connection)

app.include_router(user_module_router)
app.include_router(auth_router)
app.include_router(recipient_router)

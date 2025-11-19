from fastapi import FastAPI, Depends, Request, HTTPException, status
from pydantic import EmailStr
from typing import Dict
from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import AsyncSession


from config.database import get_async_db, async_engine, Base
from models.user import User
from controllers.database import create_meta_in_table, fetch_user_meta_with_email, fetch_user_meta_with_id

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("[x] Attempting to connect to DB before FastAPI-Server startup...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("[✅] Successfully, created the Table in the DB. if ! Existing.")

        yield
        

app = FastAPI(title="User-Service", lifespan=lifespan)


# Return the current state of the server and its external dependencies
@app.get("/health")
async def server_health():
    pass


# A POST request endpoint
@app.post("/api/v1/users/")
async def create_user(user_data: User,  db_session:AsyncSession = Depends(get_async_db)) -> Dict:
    save_status = await create_meta_in_table(db_session, user_data)
    return {"user_data": user_data,}


# A GET request by email endpoint
@app.get("/api/v1/users/{user_email}")
async def fetch_user_by_email(user_email: EmailStr, db_session:AsyncSession = Depends(get_async_db)) -> Dict:
    got_user = await fetch_user_meta_with_email(user_email, db_session)
    return {"sucess": "OK"}


# A GET request by id endpoint
@app.get("/api/v1/users/id/{user_id}")
async def get_user_by_id(user_id: str) -> Dict:
    print(user_id)
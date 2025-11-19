from fastapi import FastAPI, Depends, Request, HTTPException, status
from contextlib import asynccontextmanager
import logging
from sqlalchemy.ext.asyncio import AsyncSession


from config.database import get_async_db, async_engine, Base
from models.user import User
from controllers.database import create_meta_in_table

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("[x] Attempting to connect to DB before FastAPI-Server startup...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("[✅] Successfully, created the Table in the DB. if ! Existing.")

        yield
        

app = FastAPI(title="User-Service", lifespan=lifespan)


@app.get("/health")
async def server_health():
    pass


@app.post("/api/v1/users/")
async def create_user(user_data: User,  db_session:AsyncSession = Depends(get_async_db)):
    save_status = await create_meta_in_table(db_session, user_data)
    return {"user_data": user_data,}
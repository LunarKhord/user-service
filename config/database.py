import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
from typing import AsyncGenerator
import logging
from sqlalchemy import exc

"""
This module encapsulates the configuration and management of the PostgreSQL database connection, 
leveraging SQLAlchemy's asynchronous capabilities to yield a context-aware session for ORM operations.
"""

# --- Configuration and Initialization ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("POSTGRES_URL")

if not DATABASE_URL:
	#A missing URL is a fatal configuration error.
	logger.critical("[FATAL] POSTGRES_URL environment variable is not set. Database connection cannot be established.")
    


# The Asynchronous Engine: The primary gateway to the database.
# Setting pool_size and max_overflow is prudent for high-concurrency environments.
try:
	async_engine = create_async_engine(
		DATABASE_URL, 
		echo=False, 
		pool_size=100, 
		max_overflow=200, 
		isolation_level="REPEATABLE READ"
	)
	logger.info("✅ Asynchronous SQLAlchemy Engine successfully created.")
except Exception as e:
	logger.critical(f"[FATAL] Failed to create SQLAlchemy Engine: {e}")
 

# The Asynchronous Session Factory: Configures the behavior of new session objects.
AsyncSessionLocal = sessionmaker(
	autocommit=False,  
	autoflush=False,  
	bind=async_engine,  
	class_=AsyncSession,
    expire_on_commit=False 
)



Base = declarative_base()


# --- Dependency Injection Function ---
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    An asynchronous generator function designed to be used as a dependency (e.g., in FastAPI).
    It manages the full lifecycle of an AsyncSession: creation, yielding, transaction management, and closing.
    """
    async with AsyncSessionLocal() as db:
    	logger.debug(f"[INFO] Database session started: {db}")
    	try:
    		yield db
    		await db.commit()
    		logger.info("[INFO] Transaction committed successfully")
    	except exc.SQLAlchemyError as e:
    		logger.error(f"[ERROR] SQLAlchemy error encountered. Initiating rollback. Details: {e}")
    		raise
    	except Exception as e:
    		logger.error(f"[ERROR] None-SQLAlchemy error encountered. Initiating rollback. Details {e}")
    		await db.rollback()
    		raise
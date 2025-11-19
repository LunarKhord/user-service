import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload, joinedload
from typing import Dict
from utils.security.jwt_manager import get_hashed_password
from models.database_models import User, Preference # SQLAlchemy ORM
from models.user import UserResponse # Pydantic Model
"""
This module exist as the controller to the database, its purpose is presenting functions that interact with the Database
"""


logger = logging.getLogger(__name__)


# This function receives the user validated POST meta
# And stores it into the database
async def create_meta_in_table(db_session: AsyncSession, user_meta: User) -> Dict:

	# Hash the plain text password Sync
	password_hash = get_hashed_password(user_meta.password)

	# Extract only the preferences key with its values and exclude all others
	user_preference = user_meta.preferences.model_dump()

	# Extract all fields except for preferences, this would be stored in the Preference Table
	excluded = {"preferences", "password"}
	user_data = user_meta.model_dump(exclude=excluded)

	# Set the hashed password into the user dict.
	user_data["hashed_password"] = password_hash

	try:
		# Save to DB
		logger.info("[INFO]: Attempting to save user data to the User Table.")
		
		# Instantiate the two SQLAlchemy ORM objects, User and Preference
		new_user = User(**user_data)
		new_user_preference = Preference(**user_preference)

		# Insert the preference to the User object, this would establish the one-to-one relationship
		# SQLAlchemy automatically handles it.
		new_user.preferences = new_user_preference
		
		# Add the instace of User to the session and flush
		db_session.add(new_user)
		db_session.flush()

		logger.info(f"[INFO]: User (ID: {new_user.id}) and Preferences stored.")
		logger.info(f"[INFO]: User (ID: {new_user.id}) INFO: {new_user}.")
	except Exception as e:
		logger.error("[ERROR]: Could not store user data into User table.")
		logger.error(f"[Error]: {e}")
		print(e)


# Receive user id and returns the meata associated with the email
async def fetch_user_meta_with_email(user_email: str, db_session: AsyncSession) -> Dict:
	logger.info("[INFO]: Fetch user by Email.Executed")
	user_orm = select(User)
	user_email = user_email.strip()
	try:
		logger.info(f"[INFO]: A search has been initiated for {user_email}")
		user_orm = user_orm.where(User.email.ilike(f"{user_email}")).options(selectinload(User.preferences))
		user_orm = await db_session.execute(user_orm)

		# GET the scalar result a single ORM or NONE
		db_user_result = user_orm.scalar_one_or_none()
		logger.info(f"[INFO]: {user_email} fetched meta: {db_user_result}")
		# Pass the ORM object into a Pydantic Model.
		pydantic_payload = UserResponse.model_validate(db_user_result)
		return pydantic_payload.model_dump()

	except Exception as e:
		raise e



# Receive user id and return the meata associated with the id
async def fetch_user_meta_with_id(db_session: AsyncSession, user_id: str):
	logger.info("[INFO]: Fetch user by ID.Executed")
	user_orm = select(User)
	user_email = user_email.strip()
	try:
		logger.info(f"[INFO]: A search has been initiated for {user_id}")
		user_orm = user_orm.where(User.id.ilike(f"{user_id}")).options(selectinload(User.preferences))
		user_orm = await db_session.execute(user_orm)

		# GET the scalar result a single ORM or NONE
		db_user_result = user_orm.scalar_one_or_none()
		logger.info(f"[INFO]: {user_id} fetched meta: {db_user_result}")
		# Pass the ORM object into a Pydantic Model.
		pydantic_payload = UserResponse.model_validate(db_user_result)
		return pydantic_payload.model_dump()

	except Exception as e:
		raise e

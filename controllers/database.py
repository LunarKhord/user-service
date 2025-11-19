import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict


from utils.security.jwt_manager import get_hashed_password
from models.database_models import User, Preference
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


# This function receives a user id or a way to identify them
# And returns their full Meta.
async def fetch_user_meta_with_id():
	pass
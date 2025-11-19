import logging
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict


from utils.security.jwt_manager import get_hashed_password
from models.user import User

"""
This module exist as the controller to the database, its purpose is presenting functions that interact with the Database
"""


logger = logging.getLogger(__name__)

"""
----------REQUIRED FIELDS -----------------------
	name = Column(String(512), index=True, nullable=False)
	email = Column(String(512), index=True, unique=True, nullable=False)
	push_token = Column(String(1000), index=True, unique=False, nullable=True)
 	preferences = Column(String(30), index=True, unique=False, nullable=False)
 	hashed_password = Column(String(1000), index=True, unique=False, nullable=False)
"""

# This function receives the user validated POST meta
# And stores it into the database
async def create_meta_in_table(db_session: AsyncSession, user_meta: User) -> Dict:

	# Hash the plain text password Sync
	password_hash = get_hashed_password(user_meta.password)
	
	try:
		# Save to DB
		logger.info("[INFO]: Attempting to save user data to the User Table.")
		print(user_meta)
	# 	new_user = User(
	# 	name=user_meta.name,
	# 	email=user_meta.email,
	# 	push_token=user_meta.push_token,
	# 	preferences=user_meta.preferences,
	# 	hashed_password=password_hash
	# )
		logger.info("[INFO]: User data was stored.")
	except Exception as e:
		logger.error("[ERROR]: Could not store user data into User table.")
		logger.error(f"[Error]: {e}")
		print(e)


# This function receives a user id or a way to identify them
# And returns their full Meta.
async def fetch_user_meta_with_id():
	pass
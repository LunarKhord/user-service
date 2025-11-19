"""
The module handles all token operations (creation, verification, expiration).
"""


from argon2 import PasswordHasher

password_context = PasswordHasher()

# Return a hash from the plain text password.
def get_hashed_password(password: str) -> str:
	return password_context.hash(password)


# Verify the password and hashed version of the given password.
def verify_password(password:str, hashed_password:str)-> bool:
	return password_context.verify(password, hashed_password)
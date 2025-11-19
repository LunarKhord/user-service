from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Literal, Optional, List, Dict, Any
from uuid import UUID
from enum import Enum
from datetime import datetime
from enum import Enum


class UserPreference(BaseModel):
	email: bool = Field(True, description="Do you want to use email?")
	push: bool = Field(True, description="Do you want to use push?")


class User(BaseModel):
	name: str = Field(..., description="The name of the user")
	email: EmailStr = Field(..., description="The email of the user")
	push_token: Optional[str]  # can be updated with an update endpoint
	preferences: UserPreference
	password: str = Field(..., description="The password set by the user")
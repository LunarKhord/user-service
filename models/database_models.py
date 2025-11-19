from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone


from config.database import Base


"""This module, defines the Schema and or fields that the table will contain as colums with restrictions"""


class User(Base):
	 __tablename__ = "users"
	 id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	 name = Column(String(512), index=True, nullable=False)
	 email = Column(String(512), index=True, unique=True, nullable=False)
	 push_token = Column(String(1000), index=True, unique=False, nullable=True)
	 preferences = relationship("Preference", back_populates="user", uselist=False) # Create a one-to-one relationship between User Table and Preference Table
	 hashed_password = Column(String(1000), index=True, unique=False, nullable=False)
	 createdAt = Column(DateTime(timezone=True), default=func.now())
	 updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class Preference(Base):
	__tablename__ = "preferences"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
	email = Column(Boolean, default=True, nullable=False)
	push = Column(Boolean, default=True, nullable=False)
	user = relationship("User", back_populates="preferences")
from database import Base
from typing import List
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum, JSON, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(JSON, nullable=False)  # JSON column for storing structured data
    created_at = Column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    api_call_count = Column(Integer, default=0)
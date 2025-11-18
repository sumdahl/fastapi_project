import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    username = Column(String(length=255), unique=True, index=True, nullable=False)
    full_name = Column(String(length=255), nullable=True)
    hashed_password = Column(String(length=255), nullable=False)
    reset_token = Column(String(length=255), nullable=True, index=True)
    reset_token_expires = Column(DateTime, nullable=True)
    

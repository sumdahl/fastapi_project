import uuid
from datetime import datetime, timedelta
from typing import Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


import uuid

def get_user(db: Session, user_id: uuid.UUID) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, identifier: str, password: str) -> User | None:
    """Authenticate a user by email or username and password."""
    user = get_user_by_email(db, identifier) or get_user_by_username(db, identifier)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_with_password(
    db: Session,
    email: str,
    username: str,
    password: str,
    full_name: str | None = None
) -> User:
    """Create a new user with a hashed password."""
    hashed_password = get_password_hash(password)
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_password_reset_token_for_user(db: Session, email: str) -> str | None:
    """
    Create a password reset token for a user.
    
    Uses a secure random token (more standard than JWT for password reset).
    The token is stored as-is in the database for easy comparison.
    For production, consider hashing the token before storing.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    
    # Generate a secure random token (standard approach)
    from app.core.security import generate_password_reset_token
    reset_token = generate_password_reset_token()
    
    # Store token and expiration in database
    # Note: In production, you might want to hash the token before storing
    # For now, storing plain token for simplicity (still secure if DB is protected)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    db.refresh(user)
    
    return reset_token


def reset_user_password(db: Session, token: str, new_password: str) -> Tuple[User | None, str]:
    """
    Reset a user's password using a reset token.
    
    Standard approach: Look up user by token directly (more efficient than JWT decode).
    
    Returns:
        tuple: (User object if successful, error message if failed)
    """
    # Find user by reset token (standard approach - direct DB lookup)
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return None, "Invalid or expired reset token"
    
    # Check if token has expired
    if user.reset_token_expires is None:
        return None, "Reset token has no expiration date"
    
    if user.reset_token_expires < datetime.utcnow():
        # Clear expired token
        user.reset_token = None
        user.reset_token_expires = None
        db.commit()
        return None, "Reset token has expired"
    
    # Update password and clear reset token (single-use)
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    db.refresh(user)
    
    return user, ""

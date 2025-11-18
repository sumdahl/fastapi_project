from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import Token, UserLogin, UserRegister, ForgotPassword, ResetPassword
from app.services.user_service import (
    authenticate_user,
    create_user_with_password,
    get_user_by_email,
    get_user_by_username,
    create_password_reset_token_for_user,
    reset_user_password,
)
from app.services.email_service import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    existing_username = get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    user = create_user_with_password(
        db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    return {
        "message": "User created successfully",
        "email": user.email,
        "username": user.username,
    }


@router.post("/login", response_model=Token)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    identifier = login_data.email or login_data.username
    user = authenticate_user(db, identifier, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},  # "sub" is the standard JWT claim for subject
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password", response_model=dict, status_code=status.HTTP_200_OK)
def forgot_password(
    forgot_password_data: ForgotPassword,
    db: Session = Depends(get_db)
):
    """
    Request a password reset.
    
    This endpoint will generate a password reset token and send it via email.
    For security reasons, it always returns success even if the email doesn't exist.
    In development mode, the reset token is also returned in the response.
    """
    user = get_user_by_email(db, forgot_password_data.email)
    
    response = {
        "message": "If an account with that email exists, a password reset link has been sent."
    }
    
    # Always return success to prevent email enumeration attacks
    if user:
        reset_token = create_password_reset_token_for_user(db, forgot_password_data.email)
        if reset_token:
            # Send password reset email
            send_password_reset_email(
                email=forgot_password_data.email,
                reset_token=reset_token
            )
            # In development, also return the token for testing
            if settings.ENV == "development" or settings.DEBUG:
                response["reset_token"] = reset_token
                response["message"] += " (Development mode: token included in response)"
    
    return response


@router.post("/reset-password", response_model=dict, status_code=status.HTTP_200_OK)
def reset_password(
    reset_password_data: ResetPassword,
    db: Session = Depends(get_db)
):
    """
    Reset password using a reset token.
    
    The token should be obtained from the forgot-password endpoint via email.
    """
    user, error_message = reset_user_password(db, reset_password_data.token, reset_password_data.new_password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message or "Invalid or expired reset token"
        )
    
    return {
        "message": "Password has been reset successfully"
    }


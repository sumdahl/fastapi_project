from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.api.deps import get_db
from app.services.user_service import create_user, get_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=201)
def api_create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # A simple uniqueness check
    # For production use a unique constraint and handle IntegrityError
    # e.g. SELECT WHERE email exists to return 409
    user = create_user(db, payload)
    return user


@router.get("/{user_id}", response_model=UserRead)
def api_get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

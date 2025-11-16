from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None

    model_config = {"from_attributes": True}

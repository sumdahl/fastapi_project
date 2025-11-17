from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, model_validator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def empty_email_to_none(cls, value: str | None):
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def validate_identifier(cls, model: "UserLogin"):
        if not model.email and not model.username:
            raise ValueError("Provide either email or username")
        if model.email and model.username:
            raise ValueError("Provide only one of email or username")
        return model


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str | None = None


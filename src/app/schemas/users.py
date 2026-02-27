from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_must_be_valid(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not value.isalnum():
            raise ValueError("Password must be alphanumeric")
        return value
    


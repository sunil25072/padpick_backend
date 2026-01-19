from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# ---------- CREATE ----------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    mobile_number: str
    location: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# ---------- UPDATE ----------
class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    mobile_number: Optional[int] = Field(
        default=None,
        ge=1000000000,
        le=9999999999
    )
    location: Optional[str] = None


# ---------- RESPONSE (SAFE) ----------
class UserProfileOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    mobile_number: Optional[int]   # ✅ NULL allowed
    location: Optional[str]        # ✅ NULL allowed

    class Config:
        from_attributes = True

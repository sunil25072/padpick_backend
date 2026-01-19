from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.User import LoginSchema
from typing import List

from models.User import User
from schemas.User import (
    UserCreate,
    UserProfileOut,
    UserProfileUpdate
)
from dependencies import get_db

userrouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@userrouter.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")


    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,  # plain for now
        mobile_number=user.mobile_number,
        location=user.location
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user_id": new_user.id
    }

@userrouter.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": db_user.id
    }


@userrouter.get("/", response_model=List[UserProfileOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@userrouter.get("/{user_id}/profile", response_model=UserProfileOut)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@userrouter.put("/{user_id}/profile", response_model=UserProfileOut)
def update_user_profile(
    user_id: int,
    data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@userrouter.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

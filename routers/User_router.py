from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form
)
from sqlalchemy.orm import Session
from typing import List
from fastapi import Form, HTTPException

from models.User import User
from schemas.User import (
    LoginSchema,
    UserProfileOut,
    UserProfileUpdate
)
from dependencies import get_db

from cloudinary_config import cloudinary
import cloudinary.uploader

userrouter = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@userrouter.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    mobile_number: str = Form(...),
    location: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        if db.query(User).filter(User.username == username).first():
            raise HTTPException(status_code=400, detail="Username already registered")

        new_user = User(
            username=username,
            email=email,
            password=password,
            mobile_number=int(mobile_number),
            location=location
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "Signup successful",
            "user_id": new_user.id
        }

    except HTTPException:
        # 🔥 VERY IMPORTANT: let FastAPI handle it
        raise

    except Exception as e:
        print("🔥 SIGNUP ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error during signup"
        )
# ================= LOGIN (JSON) =================
@userrouter.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user_id": db_user.id
    }

# ================= GET ALL USERS =================
@userrouter.get("/", response_model=List[UserProfileOut])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# ================= GET USER PROFILE =================
@userrouter.get("/{user_id}/profile", response_model=UserProfileOut)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ================= UPDATE USER PROFILE =================
@userrouter.put("/{user_id}/profile", response_model=UserProfileOut)
def update_user_profile(
    user_id: int,
    data: UserProfileUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.username is not None:
        user.username = data.username

    if data.mobile_number is not None:
        user.mobile_number = data.mobile_number

    if data.location is not None:
        user.location = data.location

    db.commit()
    db.refresh(user)
    return user

# ================= UPLOAD PROFILE IMAGE =================
@userrouter.post("/{user_id}/upload-profile-image")
def upload_profile_image(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        result = cloudinary.uploader.upload(
            file.file,
            folder="padpick_profiles",
            public_id=f"user_{user_id}",
            overwrite=True
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Cloudinary upload failed")

    user.profile_img = result["secure_url"]
    db.commit()
    db.refresh(user)

    return {
        "message": "Profile image uploaded successfully",
        "profile_img": user.profile_img
    }

# ================= DELETE USER =================
@userrouter.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile_img:
        try:
            cloudinary.uploader.destroy(f"padpick_profiles/user_{user_id}")
        except:
            pass

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

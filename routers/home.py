from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.home import Home
from models.areas import Area
from schemas.home import HomeUpdate
from dependencies import get_db
import re
import cloudinary.uploader
import cloudinary_config

homerouter = APIRouter(
    prefix="/homes",
    tags=["Homes"]
)

# ================= GET HOME BY ID =================
@homerouter.get("/{home_id}")
def get_home_by_id(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    return {
        "id": home.id,
        "name": home.name,
        "price": home.price,
        "address": home.address,
        "contact_number": home.contact_number,
        "description": "WiFi, Water, Parking",
        "images": [
            home.img1,
            home.img2,
            home.img3,
            home.img4
        ]
    }
@homerouter.post("/add")
def create_home(
    name: str = Form(...),
    price: int = Form(...),
    area_id: int = Form(...),
    address: str = Form(None),
    contact_number: str = Form(...),
    user_id: int = Form(...),
    house_images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    if not re.fullmatch(r"[6-9]\d{9}", contact_number):
        raise HTTPException(400, "Invalid mobile number")

    area = db.query(Area).filter(Area.id == area_id).first()  # ✅ FIX
    if not area:
        raise HTTPException(400, "Invalid area")

    if len(house_images) != 4:
        raise HTTPException(400, "Please upload exactly 4 images")

    image_urls = []

    for img in house_images:
        try:
            img.file.seek(0)
            result = cloudinary.uploader.upload(
                img.file,
                folder="padpick/homes"
            )
            image_urls.append(result["secure_url"])
        except Exception as e:
            print("🔥 CLOUDINARY ERROR:", e)
            raise HTTPException(500, "Cloudinary upload failed")

    new_home = Home(
        name=name,
        price=price,
        address=address,
        contact_number=contact_number,
        img1=image_urls[0],
        img2=image_urls[1],
        img3=image_urls[2],
        img4=image_urls[3],
        area_id=area_id,
        user_id=user_id
    )

    db.add(new_home)
    db.commit()
    db.refresh(new_home)

    return {
        "message": "Property posted successfully",
        "home_id": new_home.id
    }


# ================= OTHER APIs =================

@homerouter.get("/by-user/{user_id}")
def get_homes_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Home).filter(Home.user_id == user_id).all()


@homerouter.get("/allhomes")
def get_all_homes(db: Session = Depends(get_db)):
    return db.query(Home).all()


@homerouter.get("/by-area/{area_id}")
def get_homes_by_area(area_id: int, db: Session = Depends(get_db)):
    return db.query(Home).filter(Home.area_id == area_id).all()


@homerouter.put("/{home_id}")
def update_home(home_id: int, home_update: HomeUpdate, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    for key, value in home_update.dict(exclude_unset=True).items():
        setattr(home, key, value)

    db.commit()
    db.refresh(home)
    return home


@homerouter.delete("/{home_id}")
def delete_home(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    db.delete(home)
    db.commit()
    return {"message": "Home deleted successfully"}

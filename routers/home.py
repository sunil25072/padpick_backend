from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.home import Home
from models.areas import Area
from schemas.home import HomeUpdate
from dependencies import get_db
import os
import shutil
import uuid
import re

homerouter = APIRouter(
    prefix="/homes",
    tags=["Homes"]
)

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# 🔹 POST PROPERTY
@homerouter.post("/add")
def create_home(
    name: str = Form(...),
    price: int = Form(...),
    area_id: int = Form(...),
    address: str = Form(None),

    # 🔥 FIXED HERE
    contact_number: str = Form(...),

    house_images: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    # ✅ MOBILE NUMBER VALIDATION (10 digits)
    if not re.fullmatch(r"[6-9]\d{9}", contact_number):
        raise HTTPException(
            status_code=400,
            detail="Mobile number must be exactly 10 digits"
        )

    # ✅ Area check
    area = db.query(Area).filter(Area.area_id == area_id).first()
    if not area:
        raise HTTPException(status_code=400, detail="Invalid area")

    images = []

    # ✅ Save max 4 images
    for img in house_images[:4]:
        unique_name = f"{uuid.uuid4()}_{img.filename}"
        path = os.path.join(UPLOAD_DIR, unique_name)

        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

        images.append(unique_name)

    # pad remaining images with None
    while len(images) < 4:
        images.append(None)

    new_home = Home(
        name=name,
        price=price,
        address=address,
        contact_number=contact_number,  # ✅ STRING
        img1=images[0],
        img2=images[1],
        img3=images[2],
        img4=images[3],
        area_id=area_id
    )

    db.add(new_home)
    db.commit()
    db.refresh(new_home)

    return {
        "message": "Property posted successfully",
        "home_id": new_home.id
    }
# 🔹 GET ALL HOMES
@homerouter.get("/allhomes")
def get_all_homes(db: Session = Depends(get_db)):
    return db.query(Home).all()


# 🔹 GET HOMES BY AREA
@homerouter.get("/by-area/{area_id}")
def get_homes_by_area(area_id: int, db: Session = Depends(get_db)):
    homes = db.query(Home).filter(Home.area_id == area_id).all()
    if not homes:
        return {"message": "No homes found"}
    return homes


# 🔹 UPDATE HOME
@homerouter.put("/{home_id}")
def update_home(home_id: int, home_update: HomeUpdate, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    if home_update.name is not None:
        home.name = home_update.name
    if home_update.price is not None:
        home.price = home_update.price
    if home_update.address is not None:
        home.address = home_update.address
    if home_update.contact_number is not None:
        home.contact_number = home_update.contact_number
    if home_update.area_id is not None:
        home.area_id = home_update.area_id

    db.commit()
    db.refresh(home)
    return home


# 🔹 DELETE HOME
@homerouter.delete("/{home_id}")
def delete_home(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    db.delete(home)
    db.commit()
    return {"message": "Home deleted successfully"}

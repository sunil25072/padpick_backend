from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from models.home import Home
from models.areas import Area
from dependencies import get_db
import re
import cloudinary.uploader
import cloudinary_config

homerouter = APIRouter(
    prefix="/homes",
    tags=["Homes"]
)

# =================================================
# 🔥 IMPORTANT:
# Specific routes MUST come first
# =================================================

# ================= GET HOMES BY AREA =================
@homerouter.get("/by-area/{area_id}")
def get_homes_by_area(area_id: int, db: Session = Depends(get_db)):
    homes = db.query(Home).filter(Home.area_id == area_id).all()
    return homes


# ================= GET HOMES BY USER =================
@homerouter.get("/by-user/{user_id}")
def get_homes_by_user(user_id: int, db: Session = Depends(get_db)):
    homes = db.query(Home).filter(Home.user_id == user_id).all()
    return homes


# ================= CREATE HOME =================
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
    # 📞 mobile validation
    if not re.fullmatch(r"[6-9]\d{9}", contact_number):
        raise HTTPException(status_code=400, detail="Invalid mobile number")

    # 🏙 area validation
    area = db.query(Area).filter(Area.area_id == area_id).first()
    if not area:
        raise HTTPException(status_code=400, detail="Invalid area")

    if len(house_images) != 4:
        raise HTTPException(status_code=400, detail="Upload exactly 4 images")

    image_urls = []

    for img in house_images:
        try:
            img.file.seek(0)
            result = cloudinary.uploader.upload(
                img.file.read(),
                folder="padpick/homes",
                resource_type="image"
            )
            image_urls.append(result["secure_url"])
        except Exception as e:
            print("🔥 CLOUDINARY ERROR:", e)
            raise HTTPException(status_code=500, detail="Cloudinary upload failed")

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


# ================= UPDATE HOME =================
@homerouter.put("/{home_id}")
def update_home(
    home_id: int,
    name: str = Form(None),
    price: int = Form(None),
    area_id: int = Form(None),
    address: str = Form(None),
    contact_number: str = Form(None),
    house_images: list[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    # 📞 mobile validation
    if contact_number:
        if not re.fullmatch(r"[6-9]\d{9}", contact_number):
            raise HTTPException(status_code=400, detail="Invalid mobile number")
        home.contact_number = contact_number

    # ✏️ text updates
    if name:
        home.name = name
    if price:
        home.price = price
    if address:
        home.address = address

    if area_id:
        area = db.query(Area).filter(Area.area_id == area_id).first()
        if not area:
            raise HTTPException(status_code=400, detail="Invalid area")
        home.area_id = area_id

    # 🖼 optional image update
    if house_images and len(house_images) > 0:
        if len(house_images) > 4:
            raise HTTPException(status_code=400, detail="Max 4 images allowed")

        image_urls = []
        for img in house_images:
            try:
                img.file.seek(0)
                result = cloudinary.uploader.upload(
                    img.file.read(),
                    folder="padpick/homes",
                    resource_type="image"
                )
                image_urls.append(result["secure_url"])
            except Exception as e:
                print("🔥 CLOUDINARY ERROR:", e)
                raise HTTPException(status_code=500, detail="Cloudinary upload failed")

        if len(image_urls) > 0: home.img1 = image_urls[0]
        if len(image_urls) > 1: home.img2 = image_urls[1]
        if len(image_urls) > 2: home.img3 = image_urls[2]
        if len(image_urls) > 3: home.img4 = image_urls[3]

    db.commit()
    db.refresh(home)

    return {
        "message": "Property updated successfully",
        "home_id": home.id
    }


# ================= DELETE HOME =================
@homerouter.delete("/{home_id}")
def delete_home(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        raise HTTPException(status_code=404, detail="Home not found")

    db.delete(home)
    db.commit()
    return {"message": "Home deleted successfully"}


# ================= GET HOME BY ID =================
# ⚠️ ALWAYS KEEP THIS LAST
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
        "area_id": home.area_id,
        "images": [
            home.img1,
            home.img2,
            home.img3,
            home.img4
        ]
}

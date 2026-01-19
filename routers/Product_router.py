from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.home import Home
from schemas.home import HomeCreate, HomeUpdate
from dependencies import get_db

productrouter = APIRouter(
    prefix="/pg",
    tags=["product"]
)

@productrouter.post("/addproduct")
def add_home(home: HomeCreate, db: Session = Depends(get_db)):
    new_home = Home(
        name=home.name,
        description=home.description,
        price=home.price,
        address=home.address,
        contact_number=home.contact_number,
        area_id=home.area_id
    )
    db.add(new_home)
    db.commit()
    db.refresh(new_home)
    return new_home


@productrouter.get("/allproduct")
def get_all_homes(db: Session = Depends(get_db)):
    return db.query(Home).all()


# ✅ THIS IS THE KEY API YOU NEED
@productrouter.get("/by-area/{area_id}")
def get_homes_by_area(area_id: int, db: Session = Depends(get_db)):
    homes = db.query(Home).filter(Home.area_id == area_id).all()
    if not homes:
        return {"message": "No homes found for this area"}
    return homes


@productrouter.put("/{product_id}")
def update_home(home_id: int, home_update: HomeUpdate, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        return {"message": "Home not found"}

    if home_update.name is not None:
        home.name = home_update.name
    if home_update.description is not None:
        home.description = home_update.description
    if home_update.price is not None:
        home.price = home_update.price
    if home_update.address is not None:
        home.address = home_update.address
    if home_update.contact_number is not None:
        home.contact_number = home_update.contact_number

    db.commit()
    db.refresh(home)
    return home


@productrouter.delete("/{product_id}")
def delete_home(home_id: int, db: Session = Depends(get_db)):
    home = db.query(Home).filter(Home.id == home_id).first()
    if not home:
        return {"message": "Home not found"}

    db.delete(home)
    db.commit()
    return {"message": "Home deleted successfully"}

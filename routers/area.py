from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from models.areas import Area
from models.home import Home          
from schemas.area import AreaCreate, AreaUpdate, AreaResponse
from schemas.home import HomeResponse   

router = APIRouter(
    prefix="/areas",
    tags=["Areas"]
)

@router.post("/", response_model=AreaResponse)
def create_area(area: AreaCreate, db: Session = Depends(get_db)):
    existing = db.query(Area).filter(Area.name == area.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Area already exists")

    new_area = Area(**area.dict())
    db.add(new_area)
    db.commit()
    db.refresh(new_area)
    return new_area


@router.get("/", response_model=list[AreaResponse])
def get_areas(db: Session = Depends(get_db)):
    return db.query(Area).all()

@router.put("/{area_id}", response_model=AreaResponse)
def update_area(
    area_id: int,
    area_data: AreaUpdate,
    db: Session = Depends(get_db)
):
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    for key, value in area_data.dict(exclude_unset=True).items():
        setattr(area, key, value)

    db.commit()
    db.refresh(area)
    return area


@router.delete("/{area_id}")
def delete_area(area_id: int, db: Session = Depends(get_db)):
    area = db.query(Area).filter(Area.id == area_id).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")

    db.delete(area)
    db.commit()
    return {"message": "Area deleted successfully"}

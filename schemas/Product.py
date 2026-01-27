from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    address: str
    mobile_number: str
    bedrooms : int
    img1 : str
    img2 : str
    img3 : str
    img4 : str
    area_id: int  


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    address: Optional[str] = None
    mobile_number: Optional[str] = None
    area_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    address: str
    mobile_number: str
    area_id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class HomeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    address: str
    contact_number: str
    img1 : str
    img2 : str
    img3 : str
    img4 : str
    area_id: int


class HomeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    area_id: Optional[int] = None

class HomeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    address: str
    contact_number: str
    area_id: int

    class Config:
        from_attributes = True
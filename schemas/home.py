from pydantic import BaseModel
from typing import Optional

class HomeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    area_id: Optional[int] = None


class HomeUpdate(BaseModel): 
    name: Optional[str] = None
    description: Optional[str] = None 
    price: Optional[int] = None 
    address: Optional[str] = None 
    contact_number: Optional[int] = None
    area_id: Optional[int] = None

class HomeResponse(BaseModel):
    id: int
    name: str
    price: int
    address: Optional[str]
    contact_number: str
    area_id: int
    img1: Optional[str]
    img2: Optional[str]
    img3: Optional[str]
    img4: Optional[str]

    class Config:
        from_attributes = True

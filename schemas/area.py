from pydantic import BaseModel

class AreaBase(BaseModel):
    name: str
    city: str
    state: str

class AreaCreate(AreaBase):
    pass

class AreaUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    state: str | None = None

class AreaResponse(AreaBase):
    id: int
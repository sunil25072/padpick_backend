from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class Area(Base):
    __tablename__ = "areas"

    area_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False)

    homes = relationship("Home", back_populates="area")

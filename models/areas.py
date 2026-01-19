from sqlalchemy import Column, Integer, String , Text
from db.session import Base
from sqlalchemy.orm import relationship

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)

    homes = relationship("Home", back_populates="area")
    products = relationship("Product", back_populates="area")
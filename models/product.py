from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    price = Column()
    address = Column(String)
    mobile_number = Column(Integer)
    bedrooms = Column(Integer)
    img1 = Column(String)
    img2 = Column(String)
    img3 = Column(String)
    img4 = Column(String)

    area_id = Column(Integer, ForeignKey("areas.id"))  
    area = relationship("Area", back_populates="products") 

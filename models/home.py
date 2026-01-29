from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.session import Base


class Home(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    price = Column(Integer, nullable=False)
    address = Column(String)
    contact_number = Column(String(10), nullable=False)

    img1 = Column(String)
    img2 = Column(String)
    img3 = Column(String)
    img4 = Column(String)

    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    area = relationship("Area", back_populates="homes")

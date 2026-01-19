from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile_number = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    password = Column(String, nullable=False)
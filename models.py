from sqlalchemy import Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "user_data"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100)) 
    surname = Column(String(100))
    email = Column(String(100))
    password = Column(String(100))
    age = Column(Integer)
    
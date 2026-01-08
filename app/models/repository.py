from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner = Column(String)
    stars = Column(Integer)
    url = Column(String, unique=True)

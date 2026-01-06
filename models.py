from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String)
    color = Column(String)
    location_found = Column(String)
    image_url = Column(String)
    status = Column(String)
    reported_by = Column(Integer, ForeignKey("users.id"))
    date_found = Column(Date)

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Group(Base):
    __tablename__ = "group"

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    location = Column(String(256))

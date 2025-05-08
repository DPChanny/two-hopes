from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Crop(Base):
    __tablename__ = "crop"

    crop_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("group.group_id"))
    name = Column(String(256))
    type = Column(String(256))
    harvest = Column(Boolean, default=False)

    group = relationship("Group")

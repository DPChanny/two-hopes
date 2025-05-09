import enum
from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from database import Base
from entities.time_mixin import TimeMixin


class CropType(enum.Enum):
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    GRAIN = "grain"
    HERB = "herb"
    FLOWER = "flower"


class Crop(Base, TimeMixin):
    __tablename__ = "crop"

    crop_id = Column(Integer, primary_key=True, autoincrement=True)

    group_id = Column(
        Integer,
        ForeignKey("group.group_id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(256), nullable=False)
    crop_type = Column(String(256), nullable=False)
    harvest = Column(Boolean, default=False, nullable=False)

    group = relationship("Group", back_populates="crops")

    posts = relationship("Post", back_populates="crop")
    schedules = relationship("Schedule", back_populates="crop")
    sensors = relationship("Sensor", back_populates="crop")

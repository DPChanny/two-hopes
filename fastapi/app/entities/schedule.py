from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Schedule(Base):
    __tablename__ = "schedule"

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(Integer, ForeignKey("crop.crop_id"))
    start_time = Column(String(256))
    end_time = Column(String(256))
    user_name = Column(String(256))

    crop = relationship("Crop")

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from database import Base


class Sensor(Base):
    __tablename__ = "sensor"

    sensor_id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(Integer, ForeignKey("crop.crop_id"))
    name = Column(String(256))
    value = Column(String(256), default="NaN")
    type = Column(String(256))

    crop = relationship("Crop", back_populates="sensors")

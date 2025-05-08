from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from database import Base


class Post(Base):
    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    crop_id = Column(Integer, ForeignKey("crop.crop_id"))
    time = Column(DateTime)
    text = Column(Text)
    image = Column(String(256))
    user_name = Column(String(256))

    crop = relationship("Crop", back_populates="posts")

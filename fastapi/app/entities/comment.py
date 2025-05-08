from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base


class Comment(Base):
    __tablename__ = "comment"

    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey("post.post_id"))
    user_name = Column(String(256))
    text = Column(Text)
    time = Column(DateTime)

    post = relationship("Post")

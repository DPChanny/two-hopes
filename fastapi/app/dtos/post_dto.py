from datetime import datetime
from pydantic import BaseModel


class PostDTO(BaseModel):
    post_id: int
    crop_id: int
    time: datetime
    text: str
    image: str
    user_name: str

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }

from pydantic import BaseModel


class AddGroupRequestDTO(BaseModel):
    name: str
    location: str

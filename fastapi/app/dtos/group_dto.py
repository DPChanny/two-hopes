from typing import Optional
from pydantic import BaseModel


class AddGroupRequestDTO(BaseModel):
    name: str
    location: str


class GroupDTO(BaseModel):
    id: int
    name: str
    location: str

    class Config:
        orm_mode = True


class GetGrouListRequestDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class GetGroupListResponseDTO(BaseModel):
    groups: list[GroupDTO]

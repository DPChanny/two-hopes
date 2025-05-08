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


class GetGroupListResponseDTO(BaseModel):
    groups: list[GroupDTO]

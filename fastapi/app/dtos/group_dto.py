from typing import List, Optional
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO
from dtos.crop_dto import CropDetailDTO


class AddGroupRequestDTO(BaseModel):
    name: str
    location: str


class GetGroupListRequestDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class GroupDTO(BaseModel):
    group_id: int
    name: str
    location: str

    model_config = {"from_attributes": True}


class GroupDetailDTO(BaseModel):
    group_id: int
    name: str
    location: str
    crops: list[CropDetailDTO]

    model_config = {"from_attributes": True}


class GetGroupListResponseDTO(BaseResponseDTO[List[GroupDTO]]):
    pass


class GetGroupDetailRequestDTO(BaseModel):
    group_id: int


class GetGroupDetailResponseDTO(BaseResponseDTO[GroupDetailDTO]):
    pass

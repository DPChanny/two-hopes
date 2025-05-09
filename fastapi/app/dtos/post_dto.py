from typing import Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO
from datetime import datetime


class PostDTO(BaseModel):
    post_id: int
    crop_id: int
    title: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AddPostRequestDTO(BaseModel):
    crop_id: int
    title: str
    content: str


class UpdatePostRequestDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class GetPostListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetPostListResponseDTO(BaseResponseDTO[List[PostDTO]]):
    pass

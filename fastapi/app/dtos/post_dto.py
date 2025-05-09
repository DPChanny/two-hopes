from typing import Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO, TimeMixin
from dtos.comment_dto import CommentDTO


class PostDTO(BaseModel):
    post_id: int
    crop_id: int
    content: str

    model_config = {"from_attributes": True}


class PostDetailDTO(PostDTO, TimeMixin):
    comments: List[CommentDTO]


class AddPostRequestDTO(BaseModel):
    crop_id: int
    content: str


class UpdatePostRequestDTO(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class GetPostListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetPostListResponseDTO(BaseResponseDTO[List[PostDTO]]):
    pass


class GetPostDetailResponseDTO(BaseResponseDTO[PostDetailDTO]):
    pass

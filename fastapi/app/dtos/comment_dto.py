from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from dtos.base_dto import BaseResponseDTO


class CommentDTO(BaseModel):
    comment_id: int
    post_id: int
    content: str
    author: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AddCommentRequestDTO(BaseModel):
    post_id: int
    content: str
    author: str


class UpdateCommentRequestDTO(BaseModel):
    content: str


class GetCommentListRequestDTO(BaseModel):
    post_id: Optional[int] = None


class GetCommentListResponseDTO(BaseResponseDTO[List[CommentDTO]]):
    pass

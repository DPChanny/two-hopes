from typing import Optional
from pydantic import BaseModel


class AddCropRequestDTO(BaseModel):
    group_id: int
    name: str
    type: str


class CropDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    type: str

    model_config = {"from_attributes": True}


class GetCropListRequestDTO(BaseModel):
    group_id: Optional[int] = None


class GetCropListResponseDTO(BaseModel):
    crops: list[CropDTO]

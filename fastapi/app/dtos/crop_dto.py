from typing import Literal, Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO, TimeMixin
from dtos.schedule_dto import ScheduleDTO
from dtos.sensor_dto import SensorDTO
from dtos.post_dto import PostDTO

CropTypeLiteral = Literal["vegetable", "fruit", "grain", "herb", "flower"]


class CropDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    crop_type: CropTypeLiteral
    harvest: bool

    model_config = {"from_attributes": True}


class CropDetailDTO(CropDTO, TimeMixin):
    posts: List[PostDTO]
    schedules: List[ScheduleDTO]
    sensors: List[SensorDTO]


class AddCropRequestDTO(BaseModel):
    group_id: int
    name: str
    crop_type: CropTypeLiteral


class GetCropListRequestDTO(BaseModel):
    group_id: Optional[int] = None


class UpdateCropRequestDTO(BaseModel):
    name: Optional[str] = None
    crop_type: Optional[CropTypeLiteral] = None
    harvest: Optional[bool] = None


class GetCropListResponseDTO(BaseResponseDTO[List[CropDTO]]):
    pass


class GetCropDetailResponseDTO(BaseResponseDTO[CropDetailDTO]):
    pass

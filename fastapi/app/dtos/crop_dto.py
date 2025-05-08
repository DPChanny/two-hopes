from typing import Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO
from dtos.schedule_dto import ScheduleDTO
from dtos.sensor_dto import SensorDTO
from dtos.post_dto import PostDTO


class AddCropRequestDTO(BaseModel):
    group_id: int
    name: str
    type: str


class CropDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    type: str
    harvest: bool

    model_config = {"from_attributes": True}


class CropDetailDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    type: str
    harvest: bool
    posts: List[PostDTO]
    schedules: List[ScheduleDTO]
    sensors: List[SensorDTO]

    model_config = {"from_attributes": True}


class GetCropListRequestDTO(BaseModel):
    group_id: Optional[int] = None


class GetCropListResponseDTO(BaseResponseDTO[List[CropDTO]]):
    pass


class GetCropDetailRequestDTO(BaseModel):
    crop_id: int


class GetCropDetailResponseDTO(BaseResponseDTO[CropDetailDTO]):
    pass

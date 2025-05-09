from typing import Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO
from dtos.schedule_dto import ScheduleDTO
from dtos.sensor_dto import SensorDTO
from dtos.post_dto import PostDTO


class CropDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    type: str
    harvest: bool

    model_config = {"from_attributes": True}


class CropDetailDTO(CropDTO):
    posts: List[PostDTO]
    schedules: List[ScheduleDTO]
    sensors: List[SensorDTO]


class AddCropRequestDTO(BaseModel):
    group_id: int
    name: str
    type: str


class GetCropListRequestDTO(BaseModel):
    group_id: Optional[int] = None


class UpdateCropRequestDTO(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    harvest: Optional[bool] = None


class GetCropListResponseDTO(BaseResponseDTO[List[CropDTO]]):
    pass


class GetCropDetailResponseDTO(BaseResponseDTO[CropDetailDTO]):
    pass

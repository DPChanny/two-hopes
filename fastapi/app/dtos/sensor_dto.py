from typing import Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO


class SensorDTO(BaseModel):
    sensor_id: int
    crop_id: int
    value: str
    name: str
    type: str

    model_config = {"from_attributes": True}


class AddSensorRequestDTO(BaseModel):
    crop_id: int
    name: str
    type: str


class GetSensorListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetSensorListResponseDTO(BaseResponseDTO[List[SensorDTO]]):
    pass

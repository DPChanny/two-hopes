from typing import Optional
from pydantic import BaseModel


class AddSensorRequestDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    image: str


class SensorDTO(BaseModel):
    sensor_id: int
    crop_id: int
    group_id: int
    name: str
    image: str

    model_config = {"from_attributes": True}


class GetSensorListResponseDTO(BaseModel):
    sensors: list[SensorDTO]


class GetSensorListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None

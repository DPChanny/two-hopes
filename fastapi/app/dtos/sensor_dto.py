from typing import Literal, Optional, List
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO, TimeMixin


SensorTypeLiteral = Literal["temperature", "humidity", "light", "ph", "co2"]


class SensorDTO(BaseModel):
    sensor_id: int
    crop_id: int

    value: str
    name: str
    sensor_type: SensorTypeLiteral

    model_config = {"from_attributes": True}


class SensorDetailDTO(SensorDTO, TimeMixin):
    pass


class AddSensorRequestDTO(BaseModel):
    crop_id: int
    name: str
    sensor_type: SensorTypeLiteral


class UpdateSensorRequestDTO(BaseModel):
    name: Optional[str] = None
    sensor_type: Optional[SensorTypeLiteral] = None
    value: Optional[str] = None


class GetSensorListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetSensorListResponseDTO(BaseResponseDTO[List[SensorDTO]]):
    pass


class GetSensorDetailResponseDTO(BaseResponseDTO[SensorDetailDTO]):
    pass

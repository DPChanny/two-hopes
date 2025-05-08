from pydantic import BaseModel


class AddSensorDTO(BaseModel):
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


class GetSensorListResponseDTO(BaseModel):
    sensors: list[SensorDTO]


class GetSensorListRequestDTO(BaseModel):
    crop_id: int

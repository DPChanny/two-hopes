from pydantic import BaseModel


class AddSensorDTO(BaseModel):
    crop_id: int
    group_id: int
    name: str
    value: str
    range: str

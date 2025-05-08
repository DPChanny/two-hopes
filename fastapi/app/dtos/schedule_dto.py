from pydantic import BaseModel
from typing import Optional


class AddScheduleRequestDTO(BaseModel):
    crop_id: int
    start_time: str
    end_time: str
    user_name: str


class ScheduleDTO(BaseModel):
    schedule_id: int
    crop_id: int
    group_id: int
    start_time: str
    end_time: str
    user_name: str

    model_config = {"from_attributes": True}


class GetScheduleListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetScheduleListResponseDTO(BaseModel):
    schedules: list[ScheduleDTO]

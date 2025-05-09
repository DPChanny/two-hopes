from datetime import time
from typing import Optional, List, Literal
from pydantic import BaseModel
from dtos.base_dto import BaseResponseDTO, TimeMixin

WeekdayLiteral = Literal["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class ScheduleDTO(BaseModel):
    schedule_id: int
    crop_id: int
    weekday: WeekdayLiteral
    start_time: time
    end_time: time
    author: str

    model_config = {"from_attributes": True}


class ScheduleDetailDTO(ScheduleDTO, TimeMixin):
    pass


class AddScheduleRequestDTO(BaseModel):
    crop_id: int
    weekday: WeekdayLiteral
    start_time: time
    end_time: time
    author: str


class UpdateScheduleRequestDTO(BaseModel):
    weekday: Optional[WeekdayLiteral] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    author: Optional[str] = None


class GetScheduleListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetScheduleListResponseDTO(BaseResponseDTO[List[ScheduleDTO]]):
    pass


class GetScheduleDetailResponseDTO(BaseResponseDTO[ScheduleDetailDTO]):
    pass

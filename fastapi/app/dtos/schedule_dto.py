from pydantic import BaseModel
from typing import Optional, List
from dtos.base_dto import BaseResponseDTO


class ScheduleDTO(BaseModel):
    schedule_id: int
    crop_id: int
    start_time: str
    end_time: str
    user_name: str

    model_config = {"from_attributes": True}


class AddScheduleRequestDTO(BaseModel):
    crop_id: int
    start_time: str
    end_time: str
    user_name: str


class GetScheduleListRequestDTO(BaseModel):
    group_id: Optional[int] = None
    crop_id: Optional[int] = None


class GetScheduleListResponseDTO(BaseResponseDTO[List[ScheduleDTO]]):
    pass

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from dtos.schedule_dto import (
    AddScheduleRequestDTO,
    GetScheduleListRequestDTO,
    GetScheduleListResponseDTO,
    ScheduleDTO,
)
from dtos.base_dto import BaseResponseDTO
from services.schedule_service import (
    add_schedule_service,
    get_schedule_list_service,
)

schedule_router = APIRouter()


@schedule_router.post("/", response_model=BaseResponseDTO[ScheduleDTO])
def add_schedule_route(
    dto: AddScheduleRequestDTO, db: Session = Depends(get_db)
):
    return add_schedule_service(dto, db)


@schedule_router.get("/", response_model=GetScheduleListResponseDTO)
def get_schedule_list_route(
    group_id: int = Query(None),
    crop_id: int = Query(None),
    db: Session = Depends(get_db),
):
    return get_schedule_list_service(
        GetScheduleListRequestDTO(group_id=group_id, crop_id=crop_id), db
    )

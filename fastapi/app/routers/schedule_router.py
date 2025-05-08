from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.schedule_dto import (
    AddScheduleRequestDTO,
    GetScheduleListRequestDTO,
    GetScheduleListResponseDTO,
)
from services.schedule_service import (
    add_schedule_service,
    get_schedule_list_service,
)

schedule_router = APIRouter()


@schedule_router.post("/schedule/add")
def add_schedule_route(
    dto: AddScheduleRequestDTO, db: Session = Depends(get_db)
):
    add_schedule_service(dto, db)


@schedule_router.get(
    "/schedule/list", response_model=GetScheduleListResponseDTO
)
def get_schedule_list_route(
    dto: GetScheduleListRequestDTO = Depends(), db: Session = Depends(get_db)
):
    return get_schedule_list_service(dto, db)

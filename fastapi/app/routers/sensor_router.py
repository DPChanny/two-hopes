from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.sensor_dto import (
    AddSensorRequestDTO,
    GetSensorListRequestDTO,
    GetSensorListResponseDTO,
)
from services.sensor_service import add_sensor_service, get_sensor_list_service

sensor_router = APIRouter()


@sensor_router.post("/sensor/add")
def add_sensor_route(dto: AddSensorRequestDTO, db: Session = Depends(get_db)):
    add_sensor_service(dto, db)


@sensor_router.post("/sensor/list", response_model=GetSensorListResponseDTO)
def get_sensor_list_route(
    dto: GetSensorListRequestDTO = Depends(), db: Session = Depends(get_db)
):
    return get_sensor_list_service(dto, db)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.sensor_dto import (
    AddSensorRequestDTO,
    GetSensorListRequestDTO,
    GetSensorListResponseDTO,
    SensorDTO,
)
from dtos.base_dto import BaseResponseDTO
from services.sensor_service import add_sensor_service, get_sensor_list_service

sensor_router = APIRouter()


@sensor_router.post("/add", response_model=BaseResponseDTO[SensorDTO])
def add_sensor_route(dto: AddSensorRequestDTO, db: Session = Depends(get_db)):
    return add_sensor_service(dto, db)


@sensor_router.post("/list", response_model=GetSensorListResponseDTO)
def get_sensor_list_route(
    dto: GetSensorListRequestDTO, db: Session = Depends(get_db)
):
    return get_sensor_list_service(dto, db)

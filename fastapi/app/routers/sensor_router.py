from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.sensor_dto import AddSensorRequestDTO
from services.sensor_service import add_sensor_service

sensor_router = APIRouter()


@sensor_router.post("/sensor/add")
def add_sensor_route(dto: AddSensorRequestDTO, db: Session = Depends(get_db)):
    add_sensor_service(dto, db)

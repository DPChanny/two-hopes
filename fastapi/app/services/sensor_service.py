from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.sensor_dto import (
    AddSensorRequestDTO,
    GetSensorListRequestDTO,
    GetSensorListResponseDTO,
)
from entities.sensor import Sensor
from entities.crop import Crop


def add_sensor_service(dto: AddSensorRequestDTO, db: Session):
    crop = db.query(Crop).filter(Crop.crop_id == dto.crop_id).first()

    db.add(
        Sensor(
            crop_id=dto.crop_id,
            group_id=crop.group_id,
            name=dto.name,
            type=dto.type,
        )
    )
    db.commit()


def get_sensor_list_service(
    dto: GetSensorListRequestDTO, db: Session
) -> GetSensorListResponseDTO:
    query = db.query(Sensor)

    if dto.group_id:
        query = query.filter(Sensor.group_id == dto.group_id)
    if dto.crop_id:
        query = query.filter(Sensor.crop_id == dto.crop_id)

    return GetSensorListResponseDTO(sensors=query.all())

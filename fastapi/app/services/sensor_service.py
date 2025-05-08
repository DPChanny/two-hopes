from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.sensor_dto import AddSensorDTO
from entities.sensor import Sensor


def add_crop_service(dto: AddSensorDTO, db: Session):
    db.add(
        Sensor(
            crop_id=dto.crop_id,
            group_id=dto.group_id,
            name=dto.name,
            image=dto.image,
        )
    )
    db.commit()

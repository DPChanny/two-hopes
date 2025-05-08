from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from dtos.sensor_dto import (
    AddSensorRequestDTO,
    GetSensorListRequestDTO,
    GetSensorListResponseDTO,
    SensorDTO,
)
from entities.sensor import Sensor
from entities.crop import Crop
from dtos.base_dto import BaseResponseDTO
from exception import CustomException


def add_sensor_service(
    dto: AddSensorRequestDTO, db: Session
) -> BaseResponseDTO[SensorDTO]:
    try:
        sensor = Sensor(crop_id=dto.crop_id, name=dto.name, type=dto.type)
        db.add(sensor)
        db.commit()
        db.refresh(sensor)

        return BaseResponseDTO(
            success=True,
            code=201,
            message="Sensor successfully added.",
            data=SensorDTO.model_validate(sensor),
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise CustomException(1400, f"DB error: {str(e)}")
    except ValidationError as e:
        raise CustomException(1401, f"Validation error: {str(e)}")


def get_sensor_list_service(
    dto: GetSensorListRequestDTO, db: Session
) -> GetSensorListResponseDTO:
    try:
        query = db.query(Sensor).join(Sensor.crop)

        if dto.group_id:
            query = query.filter(Crop.group_id == dto.group_id)
        if dto.crop_id:
            query = query.filter(Sensor.crop_id == dto.crop_id)

        sensors = query.all()
        sensor_dtos = [SensorDTO.model_validate(s) for s in sensors]

        return GetSensorListResponseDTO(
            success=True,
            code=200,
            message="Sensor list retrieved successfully.",
            data=sensor_dtos,
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise CustomException(1400, f"DB error: {str(e)}")
    except ValidationError as e:
        raise CustomException(1401, f"Validation error: {str(e)}")

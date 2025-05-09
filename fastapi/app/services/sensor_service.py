from sqlalchemy.orm import Session

from dtos.sensor_dto import (
    AddSensorRequestDTO,
    GetSensorListRequestDTO,
    GetSensorListResponseDTO,
    SensorDTO,
    UpdateSensorRequestDTO,
)
from entities.sensor import Sensor
from entities.crop import Crop
from dtos.base_dto import BaseResponseDTO
from exception import CustomException, handle_exception


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

    except Exception as e:
        handle_exception(e, db)


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

    except Exception as e:
        handle_exception(e, db)


def update_sensor_service(
    sensor_id: int, dto: UpdateSensorRequestDTO, db: Session
) -> BaseResponseDTO[SensorDTO]:
    try:
        sensor = db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
        if not sensor:
            raise CustomException(1404, "Sensor not found")

        for key, value in dto.model_dump(exclude_unset=True).items():
            setattr(sensor, key, value)

        db.commit()
        db.refresh(sensor)

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Sensor successfully updated.",
            data=SensorDTO.model_validate(sensor),
        )

    except Exception as e:
        handle_exception(e, db)


def delete_sensor_service(sensor_id: int, db: Session) -> BaseResponseDTO[None]:
    try:
        sensor = db.query(Sensor).filter(Sensor.sensor_id == sensor_id).first()
        if not sensor:
            raise CustomException(404, "Sensor not found.")

        db.delete(sensor)
        db.commit()

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Sensor deleted successfully.",
            data=None,
        )

    except Exception as e:
        handle_exception(e, db)

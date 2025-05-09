from sqlalchemy.orm import Session

from entities.schedule import Schedule
from entities.crop import Crop
from dtos.schedule_dto import (
    AddScheduleRequestDTO,
    GetScheduleListRequestDTO,
    GetScheduleListResponseDTO,
    ScheduleDTO,
)
from dtos.base_dto import BaseResponseDTO
from exception import CustomException, handle_exception


def add_schedule_service(
    dto: AddScheduleRequestDTO, db: Session
) -> BaseResponseDTO[ScheduleDTO]:
    try:
        crop = db.query(Crop).filter(Crop.crop_id == dto.crop_id).first()
        if not crop:
            raise CustomException(404, "Crop not found.")

        schedule = Schedule(
            crop_id=dto.crop_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            user_name=dto.user_name,
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)

        return BaseResponseDTO(
            success=True,
            code=201,
            message="Schedule successfully added.",
            data=ScheduleDTO.model_validate(schedule),
        )

    except Exception as e:
        handle_exception(e, db)


def get_schedule_list_service(
    dto: GetScheduleListRequestDTO, db: Session
) -> GetScheduleListResponseDTO:
    try:
        query = db.query(Schedule).join(Schedule.crop)

        if dto.group_id:
            query = query.filter(Crop.group_id == dto.group_id)
        if dto.crop_id:
            query = query.filter(Schedule.crop_id == dto.crop_id)

        schedule_entities = query.all()
        schedule_dtos = [
            ScheduleDTO.model_validate(s) for s in schedule_entities
        ]

        return GetScheduleListResponseDTO(
            success=True,
            code=200,
            message="Schedule list retrieved successfully.",
            data=schedule_dtos,
        )

    except Exception as e:
        handle_exception(e, db)

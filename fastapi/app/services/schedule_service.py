from sqlalchemy.orm import Session
from entities.schedule import Schedule
from entities.crop import Crop
from dtos.schedule_dto import (
    AddScheduleRequestDTO,
    GetScheduleListRequestDTO,
    GetScheduleListResponseDTO,
    GetScheduleDetailResponseDTO,
    ScheduleDTO,
    ScheduleDetailDTO,
    UpdateScheduleRequestDTO,
)
from dtos.base_dto import BaseResponseDTO
from exception import CustomException, handle_exception


def get_schedule_detail_service(
    schedule_id: int, db: Session
) -> GetScheduleDetailResponseDTO:
    try:
        schedule = (
            db.query(Schedule)
            .filter(Schedule.schedule_id == schedule_id)
            .first()
        )
        if not schedule:
            raise CustomException(404, "Schedule not found.")

        return GetScheduleDetailResponseDTO(
            success=True,
            code=200,
            message="Schedule detail retrieved successfully.",
            data=ScheduleDetailDTO.model_validate(schedule),
        )

    except Exception as e:
        handle_exception(e, db)


def add_schedule_service(
    dto: AddScheduleRequestDTO, db: Session
) -> GetScheduleDetailResponseDTO:
    try:
        crop = db.query(Crop).filter(Crop.crop_id == dto.crop_id).first()
        if not crop:
            raise CustomException(404, "Crop not found.")

        schedule = Schedule(
            weekday=dto.weekday,
            crop_id=dto.crop_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            author=dto.author,
        )
        db.add(schedule)
        db.commit()

        return get_schedule_detail_service(schedule.schedule_id, db)

    except Exception as e:
        handle_exception(e, db)


def update_schedule_service(
    schedule_id: int, dto: UpdateScheduleRequestDTO, db: Session
) -> GetScheduleDetailResponseDTO:
    try:
        schedule = (
            db.query(Schedule)
            .filter(Schedule.schedule_id == schedule_id)
            .first()
        )
        if not schedule:
            raise CustomException(404, "Schedule not found.")

        for key, value in dto.model_dump(exclude_unset=True).items():
            setattr(schedule, key, value)

        db.commit()

        return get_schedule_detail_service(schedule_id, db)

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


def delete_schedule_service(
    schedule_id: int, db: Session
) -> BaseResponseDTO[None]:
    try:
        schedule = (
            db.query(Schedule)
            .filter(Schedule.schedule_id == schedule_id)
            .first()
        )
        if not schedule:
            raise CustomException(404, "Schedule not found.")

        db.delete(schedule)
        db.commit()

        return BaseResponseDTO(
            success=True,
            code=200,
            message="Schedule deleted successfully.",
            data=None,
        )

    except Exception as e:
        handle_exception(e, db)

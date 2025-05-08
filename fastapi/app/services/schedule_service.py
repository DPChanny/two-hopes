from sqlalchemy.orm import Session
from entities.schedule import Schedule
from dtos.schedule_dto import (
    AddScheduleRequestDTO,
    GetScheduleListRequestDTO,
    GetScheduleListResponseDTO,
)
from entities.crop import Crop


def add_schedule_service(dto: AddScheduleRequestDTO, db: Session):
    crop = db.query(Crop).filter(Crop.crop_id == dto.crop_id).first()

    db.add(
        Schedule(
            crop_id=dto.crop_id,
            group_id=crop.group_id,
            start_time=dto.start_time,
            end_time=dto.end_time,
            user_name=dto.user_name,
        )
    )
    db.commit()


def get_schedule_list_service(
    dto: GetScheduleListRequestDTO, db: Session
) -> GetScheduleListResponseDTO:
    query = db.query(Schedule)

    if dto.group_id:
        query = query.filter(Schedule.group_id == dto.group_id)
    if dto.crop_id:
        query = query.filter(Schedule.crop_id == dto.crop_id)

    return GetScheduleListResponseDTO(schedules=query.all())

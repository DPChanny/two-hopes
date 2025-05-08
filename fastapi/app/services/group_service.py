from pydantic import ValidationError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from dtos.group_dto import (
    AddGroupRequestDTO,
    GetGroupListRequestDTO,
    GetGroupListResponseDTO,
    GetGroupDetailRequestDTO,
    GetGroupDetailResponseDTO,
    GroupDTO,
    GroupDetailDTO,
)
from entities.group import Group
from entities.crop import Crop
from exception import CustomException


def get_group_detail_service(
    dto: GetGroupDetailRequestDTO, db: Session
) -> GetGroupDetailResponseDTO:
    try:
        group = (
            db.query(Group)
            .options(
                joinedload(Group.crops).joinedload(Crop.posts),
                joinedload(Group.crops).joinedload(Crop.sensors),
                joinedload(Group.crops).joinedload(Crop.schedules),
            )
            .filter(Group.group_id == dto.group_id)
            .first()
        )

        if not group:
            raise CustomException(404, "Group not found.")

        return GetGroupDetailResponseDTO(
            success=True,
            code=200,
            message="Group detail retrieved successfully.",
            data=GroupDetailDTO.model_validate(group),
        )
    except SQLAlchemyError as e:
        raise CustomException(1400, f"DB error: {str(e)}")
    except ValidationError as e:
        raise CustomException(1401, f"Validation error: {str(e)}")


def add_group_service(
    dto: AddGroupRequestDTO, db: Session
) -> GetGroupDetailResponseDTO:
    try:
        group = Group(name=dto.name, location=dto.location)
        db.add(group)
        db.commit()
        db.refresh(group)

        return get_group_detail_service(
            GetGroupDetailRequestDTO(group_id=group.group_id), db
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise CustomException(1400, f"DB error: {str(e)}")
    except ValidationError as e:
        raise CustomException(1401, f"Validation error: {str(e)}")


def get_group_list_service(
    dto: GetGroupListRequestDTO, db: Session
) -> GetGroupListResponseDTO:
    try:
        query = db.query(Group)
        if dto.name:
            query = query.filter(Group.name.contains(dto.name))
        if dto.location:
            query = query.filter(Group.location.contains(dto.location))

        group_list = query.all()
        group_dtos = [GroupDTO.model_validate(g) for g in group_list]

        return GetGroupListResponseDTO(
            success=True,
            code=200,
            message="Group list retrieved successfully.",
            data=group_dtos,
        )
    except SQLAlchemyError as e:
        raise CustomException(1400, f"DB error: {str(e)}")
    except ValidationError as e:
        raise CustomException(1401, f"Validation error: {str(e)}")

from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.group_dto import AddGroupRequestDTO
from entities.group import Group
from dtos.group_dto import GetGroupListResponseDTO


def add_group_service(dto: AddGroupRequestDTO, db: Session):
    db.add(Group(name=dto.name, location=dto.location))
    db.commit()


def get_group_list_service(db: Session):
    return GetGroupListResponseDTO(groups=db.query(Group).all())

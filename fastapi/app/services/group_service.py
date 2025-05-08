from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.group_dto import AddGroupRequestDTO
from entities.group import Group


def add_group_service(dto: AddGroupRequestDTO, db: Session):
    db.add(Group(name=dto.name, location=dto.location))
    db.commit()
    db.close()

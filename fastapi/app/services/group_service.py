from sqlalchemy.orm import Session

from dtos.group_dto import AddGroupRequestDTO, GetGrouListRequestDTO, GroupDTO
from entities.group import Group
from dtos.group_dto import GetGroupListResponseDTO


def add_group_service(dto: AddGroupRequestDTO, db: Session):
    db.add(Group(name=dto.name, location=dto.location))
    db.commit()


def get_group_list_service(
    dto: GetGrouListRequestDTO, db: Session
) -> GetGroupListResponseDTO:
    query = db.query(Group)

    if dto.name:
        query = query.filter(Group.name.contains(dto.name))

    return GetGroupListResponseDTO(groups=query.all())

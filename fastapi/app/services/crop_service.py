from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.crop_dto import (
    AddCropRequestDTO,
    GetCropListRequestDTO,
    GetCropListResponseDTO,
)
from entities.crop import Crop


def add_crop_service(dto: AddCropRequestDTO, db: Session):
    db.add(
        Crop(
            group_id=dto.group_id, name=dto.name, humid=dto.humid, type=dto.type
        )
    )
    db.commit()


def get_crop_list_service(
    dto: GetCropListRequestDTO, db: Session
) -> GetCropListResponseDTO:
    query = db.query(Crop)

    if dto.name:
        query = query.filter(Crop.name.contains(dto.name))

    return GetCropListResponseDTO(crops=query.all())

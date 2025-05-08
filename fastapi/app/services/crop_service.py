from sqlalchemy.orm import Session
from sqlalchemy import text

from dtos.crop_dto import AddCropRequestDTO, GetCropListResponseDTO
from entities.crop import Crop


def add_crop_service(dto: AddCropRequestDTO, db: Session):
    db.add(
        Crop(
            group_id=dto.group_id, name=dto.name, humid=dto.humid, type=dto.type
        )
    )
    db.commit()


def get_crop_list_service(db: Session) -> GetCropListResponseDTO:
    return GetCropListResponseDTO(crops=db.query(Crop).all())

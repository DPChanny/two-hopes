from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from dtos.crop_dto import (
    AddCropRequestDTO,
    GetCropDetailResponseDTO,
    GetCropListRequestDTO,
    GetCropListResponseDTO,
    CropDTO,
    CropDetailDTO,
)
from entities.crop import Crop
from exception import CustomException, handle_exception


def get_crop_detail_service(
    crop_id: int, db: Session
) -> GetCropDetailResponseDTO:
    try:
        crop = (
            db.query(Crop)
            .options(
                joinedload(Crop.posts),
                joinedload(Crop.schedules),
                joinedload(Crop.sensors),
            )
            .filter(Crop.crop_id == crop_id)
            .first()
        )

        if not crop:
            raise CustomException(404, "Crop not found.")

        return GetCropDetailResponseDTO(
            success=True,
            code=200,
            message="Crop detail retrieved successfully.",
            data=CropDetailDTO.model_validate(crop),
        )

    except Exception as e:
        handle_exception(e, db)


def add_crop_service(
    dto: AddCropRequestDTO, db: Session
) -> GetCropDetailResponseDTO:
    try:
        crop = Crop(group_id=dto.group_id, name=dto.name, type=dto.type)
        db.add(crop)
        db.commit()
        db.refresh(crop)

        return get_crop_detail_service(crop.crop_id, db)

    except Exception as e:
        handle_exception(e, db)


def get_crop_list_service(
    dto: GetCropListRequestDTO, db: Session
) -> GetCropListResponseDTO:
    try:
        query = db.query(Crop)

        if dto.group_id:
            query = query.filter(Crop.group_id == dto.group_id)

        crop_entities = query.all()
        crop_dtos = [CropDTO.model_validate(crop) for crop in crop_entities]

        return GetCropListResponseDTO(
            success=True,
            code=200,
            message="Crop list retrieved successfully.",
            data=crop_dtos,
        )

    except Exception as e:
        handle_exception(e, db)

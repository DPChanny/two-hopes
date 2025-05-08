from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.crop_dto import (
    AddCropRequestDTO,
    GetCropDetailRequestDTO,
    GetCropDetailResponseDTO,
    GetCropListRequestDTO,
    GetCropListResponseDTO,
)
from services.crop_service import (
    add_crop_service,
    get_crop_list_service,
    get_crop_detail_service,
)

crop_router = APIRouter()


@crop_router.post("/add", response_model=GetCropDetailResponseDTO)
def add_crop_route(dto: AddCropRequestDTO, db: Session = Depends(get_db)):
    return add_crop_service(dto, db)


@crop_router.post("/list", response_model=GetCropListResponseDTO)
def get_crop_list_route(
    dto: GetCropListRequestDTO, db: Session = Depends(get_db)
):
    return get_crop_list_service(dto, db)


@crop_router.post("/detail", response_model=GetCropDetailResponseDTO)
def get_crop_detail_route(
    dto: GetCropDetailRequestDTO, db: Session = Depends(get_db)
):
    return get_crop_detail_service(dto, db)

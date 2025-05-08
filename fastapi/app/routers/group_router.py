from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.group_dto import (
    AddGroupRequestDTO,
    GetGroupDetailRequestDTO,
    GetGroupDetailResponseDTO,
    GetGroupListRequestDTO,
    GetGroupListResponseDTO,
)
from services.group_service import (
    add_group_service,
    get_group_list_service,
    get_group_detail_service,
)

group_router = APIRouter()


@group_router.post("/add", response_model=GetGroupDetailResponseDTO)
def add_group_route(dto: AddGroupRequestDTO, db: Session = Depends(get_db)):
    return add_group_service(dto, db)


@group_router.post("/list", response_model=GetGroupListResponseDTO)
def get_group_list_route(
    dto: GetGroupListRequestDTO, db: Session = Depends(get_db)
):
    return get_group_list_service(dto, db)


@group_router.post("/detail", response_model=GetGroupDetailResponseDTO)
def get_group_detail_route(
    dto: GetGroupDetailRequestDTO, db: Session = Depends(get_db)
):
    return get_group_detail_service(dto, db)

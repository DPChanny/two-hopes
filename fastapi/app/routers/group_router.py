from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dtos.group_dto import AddGroupRequestDTO
from services.group_service import add_group_service

group_router = APIRouter()


@group_router.post("/group/add")
def add_group_route(dto: AddGroupRequestDTO, db: Session = Depends(get_db)):
    add_group_service(dto, db)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.group_service import add_group_service

crop_router = APIRouter()


@crop_router.get("/crop/add")
def add_crop_route(db: Session = Depends(get_db)):
    return {"result": add_group_service(db)}


@crop_router.get("/crop/edit")
def add_crop_route(db: Session = Depends(get_db)):
    return {"result": add_group_service(db)}

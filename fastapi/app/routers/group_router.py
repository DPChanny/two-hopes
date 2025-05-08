from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.group_service import add_group_service

group_router = APIRouter()


@group_router.get("/api/group/add")
def get_test_route(db: Session = Depends(get_db)):
    return {"result": add_group_service(db)}

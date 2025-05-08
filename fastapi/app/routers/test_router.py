from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.test_service import get_test_service

crawling_router = APIRouter()


@crawling_router.get("/api/test")
def get_test_route(db: Session = Depends(get_db)):
    return {"result": get_test_service(db)}

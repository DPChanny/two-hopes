from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
import database

# nessesary to import all models to register them with SQLAlchemy
import entities

from exception import (
    CustomException,
    custom_exception_handler,
    validation_exception_handler,
)
from routers.group_router import group_router
from routers.crop_router import crop_router
from routers.schedule_router import schedule_router
from routers.sensor_router import sensor_router

app = FastAPI()


@app.on_event("startup")
def on_startup():
    database.init_engine()
    database.Base.metadata.create_all(bind=database.engine)


app.include_router(group_router, prefix="/api/group")
app.include_router(crop_router, prefix="/api/crop")
app.include_router(schedule_router, prefix="/api/schedule")
app.include_router(sensor_router, prefix="/api/sensor")

app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

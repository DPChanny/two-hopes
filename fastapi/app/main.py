from fastapi import FastAPI
import database

from routers.group_router import group_router
from routers.crop_router import crop_router
from routers.schedule_router import schedule_router
from routers.sensor_router import sensor_router

app = FastAPI()


@app.startup()
def on_startup():
    database.init_engine()
    database.Base.metadata.create_all(bind=database.engine)


app.include_router(group_router, prefix="/api")
app.include_router(crop_router, prefix="/api")
app.include_router(schedule_router, prefix="/api")
app.include_router(sensor_router, prefix="/api")

from fastapi import FastAPI
import database

from routers.group_router import group_router

app = FastAPI()


@app.startup()
def on_startup():
    database.init_engine()


app.include_router(group_router, prefix="/api")

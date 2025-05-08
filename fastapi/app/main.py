from fastapi import FastAPI
import database

from routers.test_router import test_router

app = FastAPI()


@app.startup()
def on_startup():
    database.init_engine()


app.include_router(test_router, prefix="/api")

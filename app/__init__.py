from fastapi import FastAPI

from app.api import include_router


def create_app():
    app = FastAPI()
    include_router(app)
    return app


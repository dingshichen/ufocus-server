from fastapi import APIRouter, FastAPI

api = APIRouter()

def include_router(app: FastAPI):
    from . import login, user
    app.include_router(api, prefix="/api")
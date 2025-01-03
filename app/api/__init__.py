from fastapi import APIRouter, FastAPI

from app.dao import SessionDep

api = APIRouter()

def include_router(app: FastAPI):
    from . import login, user
    app.include_router(api, prefix="/api")


# 获取当前登录用户 ID
def current_user_id(session: SessionDep) -> int:
    # user_id = session.get("login_user_id")
    return 1
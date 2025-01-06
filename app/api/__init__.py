from datetime import datetime, timezone, timedelta

import jwt
from fastapi import APIRouter, FastAPI
from jwt import InvalidTokenError
from starlette.requests import Request

from app.api.param.base import TokenData
from app.config import SECRET_KEY, ALGORITHM
from app.exception import CredentialsNotFound

api = APIRouter()


def include_router(app: FastAPI):
    from . import login, user
    app.include_router(api, prefix="/api")

# 创建 token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def current_user(request: Request) -> int:
    """

    :rtype: object
    """
    auth = request.headers["Authorization"]
    if auth is None:
        raise CredentialsNotFound()
    try:
        payload = jwt.decode(auth.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise CredentialsNotFound()
        return int(user_id)
    except InvalidTokenError:
        raise CredentialsNotFound()

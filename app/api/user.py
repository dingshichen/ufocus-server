from typing import Annotated

from . import api
from .param.base import Result, PageInfo
from .param.request import UserQuery, UserAdd
from .param.response import UserItem, UserDetail

from fastapi import Query

from ..dao import SessionDep
from ..service import user_service


@api.get("/user/{user_id}", tags=["用户"], name="详情", response_model_exclude_none=True, response_model=Result[UserDetail])
def load(user_id: int, session: SessionDep):
    user = user_service.load(user_id, session)
    return Result.success(user)

@api.get("/user", tags=["用户"], name="分页查询", response_model_exclude_none=True, response_model=Result[PageInfo[UserItem]])
def list_by_page(param: Annotated[UserQuery, Query()], session: SessionDep):
    page = user_service.list_by_page(param, session)
    return Result.success(page)

@api.post("/user", tags=["用户"], name="新增", response_model_exclude_none=True, response_model=Result[int])
def add(param: UserAdd, session: SessionDep):
    user = user_service.add(param, session)
    return Result.success(user)
from typing import Annotated

from . import api, current_user
from .param.base import Result, PageInfo
from .param.request import UserQuery, UserAdd
from .param.response import UserItem, UserDetail

from fastapi import Query, Request

from ..dao import SessionDep
from ..service import user_service


@api.get("/user/{user_id}", tags=["用户"], name="详情", response_model_exclude_none=True, response_model=Result[UserDetail])
async def load(user_id: int, session: SessionDep):
    user = user_service.load(user_id, session)
    return Result.success(user)

@api.get("/user", tags=["用户"], name="分页查询", response_model_exclude_none=True, response_model=Result[PageInfo[UserItem]])
async def list_by_page(param: Annotated[UserQuery, Query()], session: SessionDep):
    page = user_service.list_by_page(param, session)
    return Result.success(page)

@api.post("/user", tags=["用户"], name="新增", response_model_exclude_none=True, response_model=Result[int])
async def add(param: UserAdd, request: Request, session: SessionDep):
    create_user_id = await current_user(request)
    user_id = user_service.add(param, create_user_id, session)
    return Result.success(user_id)

@api.put("/user/{user_id}", tags=["用户"], name="修改", response_model_exclude_none=True, response_model=Result)
async def update(param: UserAdd, request: Request, session: SessionDep):
    create_user_id = await current_user(request)
    user_service.update(param, create_user_id, session)
    return Result.success()

@api.put("/user/lock/{user_id}", tags=["用户"], name="锁定", response_model_exclude_none=True, response_model=Result)
async def lock(user_id: int, request: Request, session: SessionDep):
    create_user_id = await current_user(request)
    user_service.lock(user_id, create_user_id, session)
    return Result.success()

@api.put("/user/unlock/{user_id}", tags=["用户"], name="解锁", response_model_exclude_none=True, response_model=Result)
async def unlock(user_id: int, request: Request, session: SessionDep):
    create_user_id = await current_user(request)
    user_service.unlock(user_id, create_user_id, session)
    return Result.success()

@api.delete("/user/{user_id}", tags=["用户"], name="删除", response_model_exclude_none=True, response_model=Result)
async def delete(user_id: int, session: SessionDep):
    user_service.delete(user_id, session)
    return Result.success()
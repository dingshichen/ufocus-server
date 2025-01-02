from . import api
from .param.base import Result, ResultStatus
from .param.request import Login
from ..dao import SessionDep
from ..service import user_service

@api.post("/login/password", tags=["认证"], name="登录")
async def login(param: Login, session: SessionDep) -> Result:
    user = user_service.get_by_account_no(param.account, session)
    if user is None:
        return Result.fail(ResultStatus.PASSWORD_ERROR)
    if user.certificate.password != param.password:
        return Result.fail(ResultStatus.PASSWORD_ERROR)
    if user.lock_flag:
        return Result.fail(ResultStatus.ACCOUNT_LOCKED)
    return Result.success()


@api.post("/logout", tags=["认证"], name="退出")
async def logout():
    # TODO 清除 session
    return Result.success()
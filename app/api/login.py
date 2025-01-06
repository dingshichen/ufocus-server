from datetime import timedelta

from . import api, create_access_token
from .param.base import Result, ResultStatus, Token
from .param.request import Login
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dao import SessionDep
from ..service import user_service


@api.post("/login/password", tags=["认证"], name="登录", response_model_exclude_none=True, response_model=Result)
async def login(param: Login, session: SessionDep) -> Result:
    user = user_service.get_by_account_no(param.account, session)
    if user is None:
        return Result.fail(ResultStatus.PASSWORD_ERROR)
    if not user_service.check_password(param.password, user.certificate.password):
        return Result.fail(ResultStatus.PASSWORD_ERROR)
    if user.lock_flag:
        return Result.fail(ResultStatus.ACCOUNT_LOCKED)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Result.success(Token(access_token=access_token, token_type="bearer"))




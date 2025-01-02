from . import api
from .param.base import Result, PageInfo
from .param.request import UserQuery
from .param.response import UserItem

from ..dao import SessionDep
from ..service import user_service


@api.post("/user/page", tags=["用户"], name="用户分页列表", response_model_exclude_none=True, response_model=Result[PageInfo[UserItem]])
def page_query(param: UserQuery, session: SessionDep):
    page = user_service.list_by_page(param, session)
    if len(page.rows) > 0:
        user_option_dict = user_service.dict_options({user.create_user_id for user in page.rows}, session)
        page.rows = [UserItem.to_item(user, user_option_dict[user.create_user_id]) for user in page.rows]
    return Result.success(page)


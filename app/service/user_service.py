from sqlalchemy import func
from sqlmodel import select

from ..api.param.base import PageInfo
from ..api.param.request import UserQuery
from ..api.param.response import UserOption
from ..dao import SessionDep
from ..dao.entity import User


def get_by_account_no(account_no: str, session: SessionDep) -> User | None:
    query = select(User).where(User.account_no == account_no)
    return session.exec(query).first()

def list_option_by_ids(ids: list[int] | set[int], session: SessionDep) -> list[UserOption]:
    query = select(User.user_id, User.user_name).where(User.user_id.in_(ids))
    users = session.exec(query).all()
    return [UserOption(userId=user.user_id, userName=user.user_name) for user in users]

def dict_options(ids: list[int] | set[int], session: SessionDep) -> dict[int, UserOption]:
    user_options = list_option_by_ids(ids, session)
    return {user_option.userId: user_option for user_option in user_options}

def list_by_page(param: UserQuery, session: SessionDep) -> PageInfo:
    # 查询总记录数
    query = select(func.count(User.user_id))
    if param.userName is not None:
        query = query.where(User.user_name.like(f"%{param.userName}%"))
    if param.lockFlag is not None:
        query = query.where(User.lock_flag is param.lockFlag)

    count = session.exec(query).one()

    # 查询分页数据
    query = select(User).limit(param.pageSize).offset((param.pageNo - 1) * param.pageSize)
    if param.userName is not None:
        query = query.where(User.user_name.like(f"%{param.userName}%"))
    if param.lockFlag is True:
        query = query.where(User.lock_flag is param.lockFlag)

    users = session.exec(query).all()
    return PageInfo.from_data(param, count, users)

import time

from sqlalchemy import func
from sqlmodel import select

from ..api import current_user_id
from ..api.param.base import PageInfo
from ..api.param.request import UserQuery, UserAdd
from ..api.param.response import UserOption, UserDetail, UserItem
from ..dao import SessionDep, generate_data_id
from ..dao.entity import User, UserCertificate


def get_by_account_no(account_no: str, session: SessionDep) -> User | None:
    query = select(User).where(User.account_no == account_no)
    return session.exec(query).first()

def list_option_by_ids(ids: list[int] | set[int], session: SessionDep) -> list[UserOption]:
    query = select(User.user_id, User.user_name).where(User.user_id.in_(ids))
    users = session.exec(query).all()
    return [UserOption(userId=_user.user_id, userName=_user.user_name) for _user in users]

def dict_options(ids: list[int] | set[int], session: SessionDep) -> dict[int, UserOption]:
    user_options = list_option_by_ids(ids, session)
    return {user_option.userId: user_option for user_option in user_options}

def list_by_page(param: UserQuery, session: SessionDep) -> PageInfo[UserItem]:
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
    if len(users) > 0:
        user_option_dict = dict_options({_user.create_user_id for _user in users}, session)
        users = [UserItem.to_item(_user, user_option_dict[_user.create_user_id]) for _user in users]
    return PageInfo.from_data(param, count, users)


def load(user_id: int, session: SessionDep) -> UserDetail:
    _user = session.get(User, user_id)
    user_option_dict = dict_options({_user.create_user_id, _user.update_user_id}, session)
    return UserDetail.to_detail(_user, user_option_dict[_user.create_user_id], user_option_dict[_user.update_user_id])


def add(user_add: UserAdd, session: SessionDep) -> int:
    create_user_id = current_user_id(session)
    create_time = time.localtime()
    _id = generate_data_id()
    _user = User(
        user_id=_id,
        user_name=user_add.userName,
        account_no=user_add.email,
        email=user_add.email,
        phone_no=user_add.phoneNo,
        lock_flag=False,
        create_user_id=create_user_id,
        create_time=create_time,
        update_user_id=create_user_id,
        update_time=create_time,
    )
    _user_certificate = UserCertificate(
        user_id=_id,
        password=default_password(),
    )
    session.add(_user)
    session.add(_user_certificate)
    return _id


def default_password() -> str:
    return "123456"
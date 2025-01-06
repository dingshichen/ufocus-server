import time

import bcrypt
from sqlalchemy import func
from sqlmodel import select

from ..api.param.base import PageInfo
from ..api.param.request import UserQuery, UserAdd, UserUpdate
from ..api.param.response import UserOption, UserDetail, UserItem
from ..dao import SessionDep, generate_data_id
from ..dao.entity import User, UserCertificate, UserRoleRel
from ..exception import EntityNotFound


def get_by_account_no(account_no: str, session: SessionDep) -> User | None:
    query = select(User).where(User.account_no == account_no)
    return session.exec(query).first()

def list_option_by_ids(ids: list[int] | set[int], session: SessionDep) -> list[UserOption]:
    query = select(User.user_id, User.user_name).where(User.user_id.in_(ids))
    users = session.exec(query).all()
    return [UserOption.to_option(_user) for _user in users]

# 返回 ID : Option 的字典结构
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

def load(user_id: int, session: SessionDep) -> UserDetail | None:
    _user = session.get(User, user_id)
    if not _user:
        return None
    user_option_dict = dict_options({_user.create_user_id, _user.update_user_id}, session)
    return UserDetail.to_detail(_user, user_option_dict[_user.create_user_id], user_option_dict[_user.update_user_id])

async def add(user_add: UserAdd, current_user_id: int, session: SessionDep) -> int:
    create_time = time.localtime()
    _id = generate_data_id()
    _user = User(
        user_id=_id,
        user_name=user_add.userName,
        account_no=user_add.email,
        email=user_add.email,
        phone_no=user_add.phoneNo,
        lock_flag=False,
        create_user_id=current_user_id,
        create_time=create_time,
        update_user_id=current_user_id,
        update_time=create_time,
    )
    _user_certificate = UserCertificate(
        user_id=_id,
        password=default_password(),
    )
    session.add(_user)
    session.add(_user_certificate)
    if user_add.role_ids and len(user_add.role_ids) > 0:
        _user_role_rels = [UserRoleRel(user_id=_id, role_id=role_id) for role_id in user_add.role_ids]
        session.add_all(_user_role_rels)
    session.commit()
    return _id

def update(user_update: UserUpdate, current_user_id: int, session: SessionDep):
    _user = session.get(user_update.userId)
    if not _user:
        raise EntityNotFound()
    _user.user_name = user_update.userName
    _user.email = user_update.email
    _user.phone_no = user_update.phoneNo
    _user.update_user_id = current_user_id
    _user.update_time = time.localtime()
    session.refresh(_user)
    session.commit()

def lock(user_id: int, current_user_id: int, session: SessionDep):
    _user = session.get(User, user_id)
    if not _user:
        raise EntityNotFound()
    _user.lock_flag = True
    _user.update_user_id = current_user_id
    _user.update_time = time.localtime()
    session.refresh(_user)
    session.commit()

def unlock(user_id: int, current_user_id: int, session: SessionDep):
    _user = session.get(User, user_id)
    if not _user:
        raise EntityNotFound()
    _user.lock_flag = False
    _user.update_user_id = current_user_id
    _user.update_time = time.localtime()
    session.refresh(_user)
    session.commit()

def delete(user_id: int, session: SessionDep):
    _user = session.get(User, user_id)
    if not _user:
        raise EntityNotFound()
    session.delete(_user)
    session.commit()

# 默认密码
def default_password() -> str:
    return hash_password("123456").decode()

# 密码密文
def hash_password(input_password: str) -> bytes:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(input_password.encode(), salt)
    return hashed

# 检查密码
def check_password(input_password: str, encode: str) -> bool:
    return bcrypt.checkpw(input_password.encode(), encode.encode())
from datetime import datetime

from pydantic import Field

from .base import CamelModel
from ...dao.entity import User


class UserOption(CamelModel):
    userId: int = Field(title="主键")
    userName: str = Field(title="用户名称")

    @classmethod
    def to_option(cls, user: User):
        return UserOption(userId=user.user_id, userName=user.user_name)


class UserItem(UserOption):
    accountNo: str = Field(title="账号")
    phoneNo: str | None = Field(title="手机号", default=None)
    email: str | None = Field(title="邮箱", default=None)
    lockFlag: bool = Field(title="锁定标志")
    createUser: UserOption = Field(title="创建用户")
    createTime: datetime = Field(title="创建时间")

    @classmethod
    def to_item(cls, user: User, create_user: UserOption):
        return UserItem(
            userId=user.user_id,
            userName=user.user_name,
            accountNo=user.account_no,
            phoneNo=user.phone_no,
            email=user.email,
            lockFlag=user.lock_flag,
            createUser=create_user,
            createTime=user.create_time,
        )


class UserDetail(UserItem):
    updateUser: UserOption = Field(title="更新用户")
    updateTime: datetime = Field(title="更新时间")

    @classmethod
    def to_detail(cls, user: User, create_user: UserOption, update_user: UserOption):
        return UserDetail(
            userId=user.user_id,
            userName=user.user_name,
            accountNo=user.account_no,
            phoneNo=user.phone_no,
            email=user.email,
            lockFlag=user.lock_flag,
            createUser=create_user,
            createTime=user.create_time,
            updateUser=update_user,
            updateTime=user.update_time,
        )
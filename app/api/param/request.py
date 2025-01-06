from pydantic import Field, BaseModel

from app.api.param.base import PageParam


class Login(BaseModel):
    account: str
    password: str

    def __str__(self):
        return f"account: {self.account}, password: {self.password}"


class UserQuery(PageParam):
    userName: str | None = Field(default=None, title="用户名称")
    lockFlag: bool | None = Field(default=None, title="锁定标志")

class UserAdd(BaseModel):
    email: str | None = Field(default=None, title="邮箱")
    phoneNo: str | None = Field(default=None, title="手机号")
    userName: str = Field(title="用户名称")
    role_ids: list[int] | None = Field(default=None, title="角色ID列表")

class UserUpdate(BaseModel):
    userId: int = Field(title="用户ID")
    email: str | None = Field(default=None, title="邮箱")
    phoneNo: str | None = Field(default=None, title="手机号")
    userName: str = Field(title="用户名称")
    role_ids: list[int] | None = Field(default=None, title="角色ID列表")
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
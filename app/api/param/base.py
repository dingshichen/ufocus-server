import math
from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic

from pydantic import Field, BaseModel
from typing_extensions import Optional

T = TypeVar("T")

class CamelModel(BaseModel):
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
        exclude_none = True


# 状态
class ResultStatus(Enum):
    SUCCESS = 0, "success"
    FAIL = -1, "fail"
    SYSTEM_ERROR = -1000, "系统错误"
    PASSWORD_ERROR = -1001, "账户不存在或密码错误"
    ACCOUNT_LOCKED = -1002, "账户被锁定"
    ENTITY_NOT_FOUND = -1011, "数据不存在"

    def __init__(self, code: int, desc: str):
        self._code = code
        self._desc = desc

    @property
    def code(self):
        return self._code

    @property
    def desc(self):
        return self._desc


# 结果
class Result(BaseModel, Generic[T]):
    code: int = Field(default=0, title="状态码")
    message: str = Field(default="success", title="状态信息")
    data: T | None = Field(default=None, title="数据")

    @classmethod
    def success(cls, data: T | None = None):
        return Result(code=ResultStatus.SUCCESS.code, message=ResultStatus.SUCCESS.desc, data=data)

    @classmethod
    def fail(cls, status: ResultStatus = ResultStatus.FAIL, message: Optional[str] = None):
        return Result(code=status.code, message=status if message is None else message)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


# 分页
class PageParam(CamelModel):
    pageNo: int = Field(default=1, title="页码")
    pageSize: int = Field(default=10, title="页容")


# 分页数据结构
class PageInfo(PageParam, Generic[T]):
    total: int = Field(default=0, title="总数据数")
    totalPage: int = Field(default=0, title="总页数")
    rows: list[T] | None = Field(default=None, title="数据")

    @classmethod
    def from_data(cls, page_param: PageParam, total: int, rows: Optional[list[T]]) -> "PageInfo":
        obj = PageInfo()
        obj.pageNo = page_param.pageNo
        obj.pageSize = page_param.pageSize
        obj.total = total
        obj.totalPage = math.ceil(total / obj.pageSize) if total == 0 else 0
        obj.rows = rows
        return obj



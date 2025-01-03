import os
from typing import Annotated, TypeVar, Optional, Any

from fastapi import Depends

from sqlalchemy import Integer, TypeDecorator, Dialect
from sqlmodel import Session, create_engine

from snowflake.client import get_guid


_mysql_url = os.getenv("MYSQL_URL")
_mysql_port = os.getenv("MYSQL_PORT")
_mysql_username = os.getenv("MYSQL_USERNAME")
_mysql_password = os.getenv("MYSQL_PASSWORD")
_mysql_database = os.getenv("MYSQL_DATABASE", "ufocus")

_engine = create_engine(f"mysql+pymysql://{_mysql_username}:{_mysql_password}@{_mysql_url}:{_mysql_port}/{_mysql_database}", echo=True)

def get_session():
    with Session(_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


T = TypeVar("T")

# 数据库 bit 转 bool
class BitTypeDecorator(TypeDecorator):

    impl = Integer
    cache_ok = True

    def process_bind_param(self, value: Optional[bool], dialect: Dialect) -> Any:
        if value is None:
            return None
        return 1 if value else 0

    def process_result_value(self, value: Optional[Integer], dialect: Dialect) -> Optional[bool]:
        if value is None:
            return None
        return bool(value)


# 生成雪花算法唯一ID
def generate_data_id():
    return get_guid()
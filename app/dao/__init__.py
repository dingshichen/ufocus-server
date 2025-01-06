from typing import Annotated, TypeVar, Optional, Any

from fastapi import Depends

from sqlalchemy import Integer, TypeDecorator, Dialect
from sqlmodel import Session, create_engine

from snowflake.client import get_guid

from app.config import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_URL, MYSQL_PORT, MYSQL_DATABASE

_engine = create_engine(f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DATABASE}", echo=True)

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

    def process_result_value(self, value: Optional[bytes], dialect: Dialect) -> Optional[bool]:
        if value is None:
            return None
        return bool.from_bytes(value)


# 生成雪花算法唯一ID
def generate_data_id():
    return get_guid()
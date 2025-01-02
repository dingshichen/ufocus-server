from datetime import datetime

from sqlalchemy import ForeignKey
from sqlmodel import SQLModel, Field, Column, Relationship

from . import BitTypeDecorator


# 用户角色关系
class UserRoleRel(SQLModel, table=True):
    __tablename__ = "usr_role_rel"

    user_id: int = Field(sa_column=Column("usr_id", ForeignKey("usr.usr_id"), primary_key=True))
    role_id: int = Field(sa_column=Column("role_id", ForeignKey("role.role_id"), primary_key=True))


# 角色权限关系
class RolePermissionRel(SQLModel, table=True):
    __tablename__ = "role_prmsn_rel"

    role_id: int = Field(sa_column=Column("role_id", ForeignKey("role.role_id"), primary_key=True))
    permission_id: int = Field(sa_column=Column("prmsn_id", ForeignKey("prmsn.prmsn_id"), primary_key=True))


# 用户
class User(SQLModel, table=True):
    __tablename__ = "usr"

    user_id: int = Field(sa_column=Column("usr_id", primary_key=True))
    user_name: str = Field(sa_column=Column("usr_nm"))
    account_no: str = Field(sa_column=Column("acc_no"))
    phone_no: str | None = Field(sa_column=Column("phn_no", default=None))
    email: str | None = Field(sa_column=Column("email", default=None))
    lock_flag: bool = Field(sa_column=Column("lck_flg", BitTypeDecorator))
    create_user_id: int = Field(sa_column=Column("crt_usr_id"))
    create_time: datetime = Field(sa_column=Column("crt_tm"))
    update_user_id: int = Field(sa_column=Column("upt_usr_id"))
    update_time: datetime = Field(sa_column=Column("upt_tm"))

    certificate: "UserCertificate" = Relationship(back_populates="user")
    roles: list["Role"] | None = Relationship(back_populates="users", link_model=UserRoleRel)


# 用户凭证
class UserCertificate(SQLModel, table=True):
    __tablename__ = "usr_crtfct"

    user_id: int = Field(sa_column=Column("usr_id", ForeignKey("usr.usr_id"), primary_key=True))
    password: str = Field(sa_column=Column("pwd"))

    user: User = Relationship(back_populates="certificate")


# 角色
class Role(SQLModel, table=True):
    role_id: int = Field(sa_column=Column("role_id", primary_key=True))
    role_name: str = Field(sa_column=Column("role_nm"))
    role_code: str | None = Field(sa_column=Column("role_cd"), default=None)
    create_user_id: int = Field(sa_column=Column("crt_usr_id"))
    create_time: datetime = Field(sa_column=Column("crt_tm"))
    update_user_id: int = Field(sa_column=Column("upt_usr_id"))
    update_time: datetime = Field(sa_column=Column("upt_tm"))

    users: list[User] | None = Relationship(back_populates="roles", link_model=UserRoleRel)


# 权限
class Permission(SQLModel, table=True):
    __tablename__ = "prmsn"

    permission_id: int = Field(sa_column=Column("prmsn_id", primary_key=True))
    permission_name: str = Field(sa_column=Column("prmsn_nm"))
    permission_code: str = Field(sa_column=Column("prmsn_cd"))


class TermFragment(SQLModel, table=True):
    __tablename__ = "term_fragment"
    term_id: int = Field(sa_column=Column("term_id", primary_key=True))
    word_id: int = Field(sa_column=Column("word_id", primary_key=True))
    sort_no: int = Field(sa_column=Column("sort_no"))


# 单词
class Word(SQLModel, table=True):
    word_id: int = Field(sa_column=Column("word_id", primary_key=True))
    chn_name: str = Field(sa_column=Column("chn_nm"))
    eng_name: str = Field(sa_column=Column("eng_nm"))
    eng_abbr: str = Field(sa_column=Column("eng_abbr"))
    std_word_flag: bool = Field(sa_column=Column("std_word_flg"))
    std_word_id: int | None = Field(sa_column=Column("std_word_id", default=None))
    create_user_id: int = Field(sa_column=Column("crt_usr_id"))
    create_time: datetime = Field(sa_column=Column("crt_tm"))
    update_user_id: int = Field(sa_column=Column("upt_usr_id"))
    update_time: datetime = Field(sa_column=Column("upt_tm"))


# 域
class Domain(SQLModel, table=True):
    domain_id: int = Field(sa_column=Column("domain_id", primary_key=True))
    word_id: int = Field(sa_column=Column("word_id"))
    logic_data_typ: str = Field(sa_column=Column("logic_data_typ"))
    length: int | None = Field(sa_column=Column("len", default=None))
    precision: int | None = Field(sa_column=Column("prcsn", default=None))
    default_flag: bool = Field(sa_column=Column("deflt_flg", default=False))
    create_user_id: int = Field(sa_column=Column("crt_usr_id"))
    create_time: datetime = Field(sa_column=Column("crt_tm"))
    update_user_id: int = Field(sa_column=Column("upt_usr_id"))
    update_time: datetime = Field(sa_column=Column("upt_tm"))


# 用语
class Term(SQLModel, table=True):
    term_id: int = Field(sa_column=Column("term_id", primary_key=True))
    chn_name: str = Field(sa_column=Column("chn_nm"))
    eng_name: str = Field(sa_column=Column("eng_nm"))
    eng_abbr: str = Field(sa_column=Column("eng_abbr"))
    std_term_flag: bool = Field(sa_column=Column("std_term_flg"))
    create_user_id: int = Field(sa_column=Column("crt_usr_id"))
    create_time: datetime = Field(sa_column=Column("crt_tm"))
    update_user_id: int = Field(sa_column=Column("upt_usr_id"))
    update_time: datetime = Field(sa_column=Column("upt_tm"))
create database ufocus default character set utf8mb4;

use ufocus;

/********************************************************
    Table  Name    :    用户
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS usr
(
    usr_id BIGINT NOT NULL COMMENT '用户ID' ,
    usr_nm VARCHAR(120) NOT NULL COMMENT '用户姓名' ,
    acc_no VARCHAR(30) NOT NULL COMMENT '账号' ,
    phn_no VARCHAR(11) COMMENT '手机号码' ,
    email VARCHAR(30) COMMENT '电子邮箱' ,
    lck_flg BIT NOT NULL COMMENT '锁定标志' ,
    crt_usr_id BIGINT NOT NULL COMMENT '创建用户ID' ,
    crt_tm DATETIME NOT NULL COMMENT '创建时间' ,
    upt_usr_id BIGINT NOT NULL COMMENT '更新用户ID' ,
    upt_tm DATETIME NOT NULL COMMENT '更新时间' ,
    PRIMARY KEY (usr_id),
    UNIQUE udx_acc (acc_no)
)
    COMMENT '用户'
;

/********************************************************
    Table  Name    :    用户凭证
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS usr_crtfct
(
    usr_id BIGINT NOT NULL COMMENT '用户ID' ,
    pwd VARCHAR(120) NOT NULL COMMENT '密码' ,
    rmbr_me_srs VARCHAR(120) COMMENT '记住我服务' ,
    rmbr_me_tkn VARCHAR(120) COMMENT '记住我令牌' ,
    rmbr_me_latest_use_tm DATETIME COMMENT '记住我最近使用时间' ,
    PRIMARY KEY (usr_id)
)
    COMMENT '用户凭证'
;

/********************************************************
    Table  Name    :    角色
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS role
(
    role_id BIGINT NOT NULL COMMENT '角色ID' ,
    role_nm VARCHAR(30) NOT NULL COMMENT '角色名称' ,
    role_cd VARCHAR(20) COMMENT '角色编码' ,
    crt_usr_id BIGINT NOT NULL COMMENT '创建用户ID' ,
    crt_tm DATETIME NOT NULL COMMENT '创建时间' ,
    upt_usr_id BIGINT NOT NULL COMMENT '更新用户ID' ,
    upt_tm DATETIME NOT NULL COMMENT '更新时间' ,
    PRIMARY KEY (role_id)
)
    COMMENT '角色'
;

/********************************************************
    Table  Name    :    用户角色关系
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS usr_role_rel
(
    usr_id BIGINT NOT NULL COMMENT '用户ID' ,
    role_id BIGINT NOT NULL COMMENT '角色ID' ,
    PRIMARY KEY (role_id,usr_id)
)
    COMMENT '用户角色关系'
;

/********************************************************
    Table  Name    :    权限
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS prmsn
(
    prmsn_id BIGINT NOT NULL COMMENT '权限ID' ,
    prmsn_nm VARCHAR(30) NOT NULL COMMENT '权限名称' ,
    prmsn_cd VARCHAR(20) NOT NULL COMMENT '权限编码' ,
    PRIMARY KEY (prmsn_id)
)
    COMMENT '权限'
;

/********************************************************
    Table  Name    :    角色权限关系
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS role_prmsn_rel
(
    role_id BIGINT NOT NULL COMMENT '角色ID' ,
    prmsn_id BIGINT NOT NULL COMMENT '权限ID' ,
    PRIMARY KEY (role_id,prmsn_id)
)
    COMMENT '角色权限关系'
;

insert into usr (usr_id, usr_nm, acc_no, lck_flg, crt_usr_id, crt_tm, upt_usr_id, upt_tm)
values (100000000, '超级管理员', 'admin', 0, 100000000, now(), 100000000, now());

insert into usr_crtfct (usr_id, pwd)
values (100000000, '{bcrypt}$2a$10$hK2mQGxf/FL0gY8Nnk87zuwZGbUednLSx3GKnr7GHU.RTF242f6dK');

insert into prmsn (prmsn_id, prmsn_nm, prmsn_cd)
values (12000001, '用户查看', 'USER_VIEW'), (12000002, '用户管理', 'USER_MANAGE'),
       (12000003, '角色查看', 'ROLE_VIEW'), (12000004, '角色管理', 'ROLE_MANAGE');

insert into role (role_id, role_nm, role_cd, crt_usr_id, crt_tm, upt_usr_id, upt_tm)
values (100000000, '超级管理员', 'S_ADMIN', 100000000, now(), 100000000, now());

insert into role_prmsn_rel (role_id, prmsn_id)
values (100000000, 12000001), (100000000, 12000002), (100000000, 12000003), (100000000, 12000004);

insert into usr_role_rel (usr_id, role_id)
values (100000000, 100000000);


/********************************************************
    Table  Name    :    单词
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS word
(
    word_id BIGINT NOT NULL COMMENT '单词ID' ,
    chn_nm VARCHAR(30) NOT NULL COMMENT '中文名称' ,
    eng_nm VARCHAR(200) NOT NULL COMMENT '英文名称' ,
    eng_abbr VARCHAR(30) NOT NULL COMMENT '英文缩写' ,
    std_word_flg BIT NOT NULL COMMENT '标准单词标志' ,
    std_word_id BIGINT COMMENT '标准单词ID' ,
    crt_usr_id BIGINT NOT NULL COMMENT '创建用户ID' ,
    crt_tm DATETIME NOT NULL COMMENT '创建时间' ,
    upt_usr_id BIGINT NOT NULL COMMENT '更新用户ID' ,
    upt_tm DATETIME NOT NULL COMMENT '更新时间' ,
    PRIMARY KEY (word_id)
)
    COMMENT '单词'
;


/********************************************************
    Table  Name    :    用语词素
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS term_fragment
(
    term_id BIGINT NOT NULL COMMENT '用语ID' ,
    word_id BIGINT NOT NULL COMMENT '单词ID' ,
    sort_no INT NOT NULL COMMENT '顺序号' ,
    PRIMARY KEY (term_id,word_id)
)
    COMMENT '用语词素'
;

/********************************************************
    Table  Name    :    域
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS domain
(
    domain_id BIGINT NOT NULL COMMENT '域ID' ,
    word_id BIGINT NOT NULL COMMENT '单词ID' ,
    logic_data_typ VARCHAR(20) NOT NULL COMMENT '逻辑数据类型' ,
    len BIGINT COMMENT '长度' ,
    prcsn BIGINT COMMENT '精度' ,
    deflt_flg BIT NOT NULL COMMENT '默认标志' ,
    crt_usr_id BIGINT NOT NULL COMMENT '创建用户ID' ,
    crt_tm DATETIME NOT NULL COMMENT '创建时间' ,
    upt_usr_id BIGINT NOT NULL COMMENT '更新用户ID' ,
    upt_tm DATETIME NOT NULL COMMENT '更新时间' ,
    PRIMARY KEY (domain_id)
)
    COMMENT '域'
;

/********************************************************
    Table  Name    :    用语
    Create Date    :    2024年12月18日
********************************************************/
CREATE TABLE IF NOT EXISTS term
(
    term_id BIGINT NOT NULL COMMENT '用语ID' ,
    chn_nm VARCHAR(30) NOT NULL COMMENT '中文名称' ,
    eng_nm VARCHAR(200) NOT NULL COMMENT '英文名称' ,
    eng_abbr VARCHAR(30) NOT NULL COMMENT '英文缩写' ,
    std_term_flg BIT NOT NULL COMMENT '标准用语标志' ,
    crt_usr_id BIGINT NOT NULL COMMENT '创建用户ID' ,
    crt_tm DATETIME NOT NULL COMMENT '创建时间' ,
    upt_usr_id BIGINT NOT NULL COMMENT '更新用户ID' ,
    upt_tm DATETIME NOT NULL COMMENT '更新时间' ,
    PRIMARY KEY (term_id)
)
    COMMENT '用语'
;
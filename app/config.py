import os

MYSQL_URL = os.getenv("MYSQL_URL", "127.0.0.1")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ufocus")

# single 单机、cluster 集群
SERVER_MODEL = os.getenv("UF_SERVER_MODEL", "single")

SECRET_KEY = "544b030df58a87cecdde2b3b55e06536611e138437d9f1c7eaec846d2499de90"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

def is_single_model() -> bool:
    return SERVER_MODEL == "single"
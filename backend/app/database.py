import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 从环境变量获取数据库 URL，如果没有则使用默认值（本地开发用）
# 注意：Docker 内部服务名是 'db'，端口是 3306
DEFAULT_DB_URL = "mysql+pymysql://bloguser:blogpassword@localhost:3307/blog_db?charset=utf8mb4"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

if "charset=utf8mb4" not in SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL += "?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # 打印 SQL 日志
    connect_args={"connect_timeout": 5}  # 5秒连接超时
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 依赖项：用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

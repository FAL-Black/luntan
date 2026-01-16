from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 获取数据库配置，如果环境变量未设置，则使用默认值
# 建议在生产环境中使用环境变量设置密码
DB_USER = os.getenv("DB_USER", "luntan_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "luntan")

# MySQL 连接字符串
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# SQLite 配置 (已注释)
# SQLALCHEMY_DATABASE_URL = "sqlite:///./luntan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    # SQLite 需要 check_same_thread，MySQL 不需要
    # connect_args={"check_same_thread": False} 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os
from sqlalchemy import create_engine, MetaData
from database import SQLALCHEMY_DATABASE_URL

# 强制重置数据库结构
def reset_database():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    meta = MetaData()
    meta.reflect(bind=engine)
    
    print("正在删除旧表...")
    meta.drop_all(bind=engine)
    
    print("旧表已删除。请重启后端服务以重新创建新表。")

if __name__ == "__main__":
    reset_database()

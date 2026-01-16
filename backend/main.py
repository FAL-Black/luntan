from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, database

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# 配置 CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

@app.get("/api/")
def read_api_root():
    return {"message": "Hello from FastAPI backend (via /api)!"}

@app.get("/api/info")
def get_info():
    return {
        "forum_name": "My Tech Forum",
        "version": "1.0.0",
        "status": "running"
    }

# 测试接口：列出所有用户
@app.get("/api/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    # posts: List[Post] = [] # 暂时注释，避免循环依赖或加载过多数据

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_original: bool = True
    is_pinned: bool = False

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner_username: Optional[str] = None
    owner_avatar: Optional[str] = None # 作者头像
    views: int = 0
    likes_count: int = 0
    comments_count: int = 0
    is_liked: bool = False # 当前用户是否点赞 (需要后端逻辑填充)
    is_collected: bool = False # 当前用户是否收藏

    class Config:
        from_attributes = True

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    owner_id: int
    post_id: int
    created_at: datetime
    owner_username: Optional[str] = None
    owner_avatar: Optional[str] = None

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    bio: Optional[str] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    avatar_url: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    avatar_url: Optional[str] = None
    followers_count: int = 0
    following_count: int = 0
    is_following: bool = False # 当前用户是否关注

    class Config:
        from_attributes = True

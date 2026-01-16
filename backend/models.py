from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# 多对多关系表：点赞
post_likes = Table('post_likes', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)

# 多对多关系表：收藏
post_collections = Table('post_collections', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
)

# 多对多关系表：关注
user_follows = Table('user_follows', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # 新增字段
    bio = Column(String(500), nullable=True) # 简介
    gender = Column(String(10), nullable=True) # 性别
    location = Column(String(100), nullable=True) # 所在地
    website = Column(String(255), nullable=True) # 个人网站

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    
    # 关系
    liked_posts = relationship("Post", secondary=post_likes, back_populates="liked_by_users")
    collected_posts = relationship("Post", secondary=post_collections, back_populates="collected_by_users")
    
    followers = relationship(
        "User", 
        secondary=user_follows,
        primaryjoin=id==user_follows.c.followed_id,
        secondaryjoin=id==user_follows.c.follower_id,
        backref="following"
    )

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 新增字段
    views = Column(Integer, default=0) # 阅读量
    category = Column(String(50), nullable=True) # 分类
    tags = Column(String(255), nullable=True) # 标签 (逗号分隔)
    is_pinned = Column(Boolean, default=False) # 置顶
    is_original = Column(Boolean, default=True) # 是否原创

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    
    liked_by_users = relationship("User", secondary=post_likes, back_populates="liked_posts")
    collected_by_users = relationship("User", secondary=post_collections, back_populates="collected_posts")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

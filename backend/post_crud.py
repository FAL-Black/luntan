from sqlalchemy.orm import Session
import models, schemas

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    # 填充用户名
    for post in posts:
        post.owner_username = post.owner.username
    return posts

def get_posts_by_user(db: Session, user_id: int):
    posts = db.query(models.Post).filter(models.Post.owner_id == user_id).order_by(models.Post.created_at.desc()).all()
    for post in posts:
        post.owner_username = post.owner.username
    return posts

def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db_post.owner_username = db_post.owner.username if db_post.owner else "Unknown"
    return db_post

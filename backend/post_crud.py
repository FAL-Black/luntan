from sqlalchemy.orm import Session
import models, schemas

def enrich_post(post, current_user_id: int = None):
    if not post:
        return
    post.owner_username = post.owner.username if post.owner else "Unknown"
    post.owner_avatar = post.owner.avatar_url if post.owner else None
    post.likes_count = len(post.liked_by_users)
    post.comments_count = len(post.comments)
    
    if current_user_id:
        post.is_liked = any(u.id == current_user_id for u in post.liked_by_users)
        post.is_collected = any(u.id == current_user_id for u in post.collected_by_users)
    else:
        post.is_liked = False
        post.is_collected = False

def get_posts(db: Session, skip: int = 0, limit: int = 100, current_user_id: int = None, category: str = None):
    query = db.query(models.Post)
    if category:
        query = query.filter(models.Post.category == category)
        
    # Sort by pinned first, then date
    posts = query.order_by(models.Post.is_pinned.desc(), models.Post.created_at.desc()).offset(skip).limit(limit).all()
    
    for post in posts:
        enrich_post(post, current_user_id)
    return posts

def get_posts_by_user(db: Session, user_id: int, current_user_id: int = None):
    posts = db.query(models.Post).filter(models.Post.owner_id == user_id).order_by(models.Post.created_at.desc()).all()
    for post in posts:
        enrich_post(post, current_user_id)
    return posts

def get_post(db: Session, post_id: int, current_user_id: int = None):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        # Increase view count
        post.views += 1
        db.commit()
        enrich_post(post, current_user_id)
    return post

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
    enrich_post(db_post, user_id)
    return db_post

def like_post(db: Session, post_id: int, user_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if post and user:
        if user not in post.liked_by_users:
            post.liked_by_users.append(user)
            db.commit()
            return True
        else:
            post.liked_by_users.remove(user)
            db.commit()
            return False # Unliked
    return None

def collect_post(db: Session, post_id: int, user_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if post and user:
        if user not in post.collected_by_users:
            post.collected_by_users.append(user)
            db.commit()
            return True
        else:
            post.collected_by_users.remove(user)
            db.commit()
            return False # Uncollected
    return None

from sqlalchemy.orm import Session
import models, schemas, auth

def enrich_user(user, current_user_id: int = None):
    if not user: return
    user.followers_count = len(user.followers)
    user.following_count = len(user.following)
    if current_user_id:
        user.is_following = any(u.id == current_user_id for u in user.followers)
    else:
        user.is_following = False

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_avatar(db: Session, user_id: int, avatar_url: str):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.avatar_url = avatar_url
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user_profile(db: Session, user_id: int, profile: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = profile.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def follow_user(db: Session, follower_id: int, followed_id: int):
    follower = get_user(db, follower_id)
    followed = get_user(db, followed_id)
    if follower and followed:
        if followed not in follower.following:
            follower.following.append(followed)
            db.commit()
            return True
        else:
            follower.following.remove(followed)
            db.commit()
            return False # Unfollowed
    return None

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

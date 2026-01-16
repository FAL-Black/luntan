import os
import shutil
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional
import models, schemas, database, auth, crud, post_crud, comment_crud

# 创建数据库表
models.Base.metadata.create_all(bind=database.engine)

# 确保上传目录存在
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI()

# 挂载静态文件目录，用于访问上传的图片
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

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

# --- 认证路由 ---

@app.post("/api/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_email = crud.get_user_by_email(db, email=user.email)
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/api/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    crud.enrich_user(current_user, current_user.id)
    return current_user

@app.put("/api/users/me", response_model=schemas.User)
def update_profile(profile: schemas.UserUpdate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    updated_user = crud.update_user_profile(db, current_user.id, profile)
    crud.enrich_user(updated_user, current_user.id)
    return updated_user

@app.put("/api/users/me/avatar", response_model=schemas.User)
def update_avatar(avatar_url: str, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.update_user_avatar(db, current_user.id, avatar_url)

@app.get("/api/users/me/posts", response_model=list[schemas.Post])
def read_my_posts(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return post_crud.get_posts_by_user(db, current_user.id, current_user.id)

@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user_profile(user_id: int, current_user: Optional[schemas.User] = Depends(auth.get_current_user_optional), db: Session = Depends(database.get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_user_id = current_user.id if current_user else None
    crud.enrich_user(user, current_user_id)
    return user

@app.post("/api/users/{user_id}/follow")
def follow_user(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    is_following = crud.follow_user(db, current_user.id, user_id)
    if is_following is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"is_following": is_following}

# --- 管理员路由 ---
@app.get("/api/admin/users", response_model=list[schemas.User])
def get_all_users(current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_all_users(db)

# --- 文件上传 ---
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    # 返回相对路径，假设前端通过 /uploads/filename 访问
    # 注意：生产环境应使用完整的 URL 或 CDN
    return {"url": f"/uploads/{file.filename}"}

# --- 帖子路由 ---

@app.post("/api/posts/", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    return post_crud.create_user_post(db=db, post=post, user_id=current_user.id)

@app.get("/api/posts/", response_model=list[schemas.Post])
def read_posts(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    current_user: Optional[schemas.User] = Depends(auth.get_current_user_optional),
    db: Session = Depends(database.get_db)
):
    current_user_id = current_user.id if current_user else None
    posts = post_crud.get_posts(db, skip=skip, limit=limit, current_user_id=current_user_id, category=category)
    return posts

@app.get("/api/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, current_user: Optional[schemas.User] = Depends(auth.get_current_user_optional), db: Session = Depends(database.get_db)):
    current_user_id = current_user.id if current_user else None
    post = post_crud.get_post(db, post_id, current_user_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/api/posts/{post_id}/like")
def like_post(post_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    result = post_crud.like_post(db, post_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"is_liked": result}

@app.post("/api/posts/{post_id}/collect")
def collect_post(post_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    result = post_crud.collect_post(db, post_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"is_collected": result}

@app.delete("/api/posts/{post_id}")
def delete_post(
    post_id: int, 
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(auth.get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 只有作者或管理员可以删除
    if post.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    post_crud.delete_post(db, post_id)
    return {"message": "Post deleted"}

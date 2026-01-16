import models
import database
import auth
from sqlalchemy.orm import Session

def create_admin():
    db = database.SessionLocal()
    try:
        username = "admin"
        password = "123456"
        email = "admin@luntan.com"
        
        # 检查是否已存在
        user = db.query(models.User).filter(models.User.username == username).first()
        if user:
            print(f"用户 {username} 已存在，正在更新为管理员权限...")
            user.is_superuser = True
            user.hashed_password = auth.get_password_hash(password) # 重置密码
            db.commit()
            print("更新完成。")
        else:
            print(f"正在创建管理员用户 {username} ...")
            hashed_password = auth.get_password_hash(password)
            new_user = models.User(
                username=username,
                email=email,
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=True
            )
            db.add(new_user)
            db.commit()
            print("管理员创建成功！")
            
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # 确保表存在
    models.Base.metadata.create_all(bind=database.engine)
    create_admin()

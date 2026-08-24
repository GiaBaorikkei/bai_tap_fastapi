from app.models.user import User
from app.schemas.user import CreateUser
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        salt
    )
    
    return hashed_password.decode("utf-8")

def get_user(db):
    user = db.query(User).all()
    return {
        "message": "Lấy tất cả người dùng thành công!",
        "data": user
    }
    
def create_user(user:CreateUser, db):
    new_user = User(
        username = user.username,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "Tạo người dùng thành công!",
        "data": new_user
    }
from fastapi import (APIRouter,Depends,status,HTTPException)
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from database import get_db
from user import User

from auth import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    LoginResponse
)

from app.services.auth_service import (
    register_user,
    login_user
)

from app.security.security import (
    get_user_id_from_token
)

from fastapi.security import HTTPAuthorizationCredentials


router_auth = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()


@router_auth.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=dict
)
def register(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):

    user = register_user(
        user_data,
        db
    )

    return {
        "message": "Đăng ký tài khoản thành công",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }
    }


@router_auth.post(
    "/login",
    response_model=LoginResponse
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    return login_user(
        login_data,
        db
    )


@router_auth.get(
    "/me",
    response_model=UserResponse
)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    # Lấy user_id từ JWT
    user_id = get_user_id_from_token(
        credentials
    )

    # Truy vấn lại database
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Người dùng không tồn tại"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="Tài khoản đã bị khóa"
        )

    return user